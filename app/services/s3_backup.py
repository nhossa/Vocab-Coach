"""
S3 Backup Service - Backs up PostgreSQL database to AWS S3.

Intended usage:
- Only active when ENVIRONMENT=production
- In dev, this becomes a no-op and clearly reports that backups are disabled
"""

import os
import boto3
from datetime import datetime, timezone
import subprocess
from urllib.parse import urlparse


class S3BackupService:
    """Service that knows how to dump the database and upload the dump to S3."""

    def __init__(self) -> None:
        """
        Initialize the S3 client only when running in production.

        Logic:
        - Read ENVIRONMENT env var (default to 'development')
        - If 'production', try to build an S3 client and load bucket name
        - If anything S3 related is missing, disable backups cleanly
        """
        self.s3_client = None
        self.bucket_name: str | None = None

        environment = os.getenv("ENVIRONMENT", "development")

        if environment == "production":
            # Bucket name must be set in production for backups to work
            bucket = os.getenv("S3_BACKUP_BUCKET")
            if not bucket:
                print(
                    "Production mode but S3_BACKUP_BUCKET is not set. "
                    "S3 backups will be disabled."
                )
                return

            # Build S3 client using configured credentials
            self.s3_client = boto3.client(
                "s3",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
            self.bucket_name = bucket
            print(f"Production mode. S3 backups enabled for bucket: {self.bucket_name}")
        else:
            # In dev or test, we do not want to accidentally write to S3
            print("Non-production mode. S3 backups are disabled.")

    def create_backup(self) -> dict:
        """
        Create a database backup using pg_dump and upload it to S3.

        Returns:
            dict with:
                - success: bool
                - message: str
        """
        # S3 client or bucket missing means backups are not configured
        if not self.s3_client or not self.bucket_name:
            return {
                "success": False,
                "message": "S3 backup not available (environment is not production or S3 not configured).",
            }

        # Create a timestamped filename for the backup
        # Example: vocab_coach_backup_20251208_143022.sql
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_filename = f"vocab_coach_backup_{timestamp}.sql"
        local_path = f"/tmp/{backup_filename}"

        print(f"Creating database backup: {backup_filename}")

        try:
            # Step 1: Read DATABASE_URL from environment
            # Example: postgresql://user:pass@host:5432/dbname
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                return {
                    "success": False,
                    "message": "DATABASE_URL is not set.",
                }

            # Step 2: Parse DATABASE_URL safely
            parsed = urlparse(db_url)

            user = parsed.username
            password = parsed.password
            host = parsed.hostname or "localhost"
            port = str(parsed.port or 5432)
            dbname = parsed.path.lstrip("/")  # removes leading "/"

            # Basic validation of parsed parts
            if not all([user, password, dbname]):
                return {
                    "success": False,
                    "message": "DATABASE_URL is missing username, password, or database name.",
                }

            # Step 3: Build pg_dump command
            # This will create a plain SQL dump at local_path
            pg_dump_cmd = [
                "pg_dump",
                "-h",
                host,
                "-p",
                port,
                "-U",
                user,
                "-d",
                dbname,
                "-F",
                "p",  # plain SQL format
                "-f",
                local_path,
            ]

            # Pass the password via PGPASSWORD so pg_dump does not prompt
            env = os.environ.copy()
            env["PGPASSWORD"] = password

            result = subprocess.run(
                pg_dump_cmd,
                env=env,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                # Log the stderr to stdout for debugging
                print(f"pg_dump failed: {result.stderr}")
                return {
                    "success": False,
                    "message": f"pg_dump failed: {result.stderr}",
                }

            print(f"Database dumped successfully to: {local_path}")

            # Step 4: Upload the dump to S3
            s3_key = f"backups/{backup_filename}"
            try:
                # local_path: path to the file on the server
                # self.bucket_name: S3 bucket name
                # s3_key: path inside the bucket
                self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
                print(f"Uploaded backup to s3://{self.bucket_name}/{s3_key}")

                # Remove the local file after successful upload
                os.remove(local_path)

            except Exception as upload_error:
                print(f"S3 upload failed: {upload_error}")
                return {
                    "success": False,
                    "message": f"S3 upload failed: {upload_error}",
                }

            return {
                "success": True,
                "message": f"Backup uploaded to s3://{self.bucket_name}/{s3_key}",
            }

        except Exception as e:
            # Catch any unexpected error and report it
            print(f"Backup failed: {e}")
            return {
                "success": False,
                "message": f"Backup failed: {str(e)}",
            }


# Single shared instance to be imported and used by the rest of the app.
# Example:
# from app.services.s3_backup import s3_backup_service
# s3_backup_service.create_backup()
s3_backup_service = S3BackupService()
