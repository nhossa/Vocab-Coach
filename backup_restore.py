#!/usr/bin/env python3
"""
StackTutor Database Backup & Restore Helper

This script helps backup and restore the PostgreSQL database to/from AWS S3.
Usage:
    python backup_restore.py backup     # Create and upload backup to S3
    python backup_restore.py restore    # Restore latest backup from S3
    python backup_restore.py list       # List all backups in S3
"""

import os
import sys
import subprocess
from datetime import datetime
import boto3
from dotenv import load_dotenv

load_dotenv()

# Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BACKUP_BUCKET", "stacktutor-backups")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "vocabuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB", "vocabdb")

s3_client = boto3.client("s3", region_name=AWS_REGION)


def backup_database():
    """Create a database backup and upload to S3."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"stacktutor_db_{timestamp}.sql"
    
    print(f"📦 Starting database backup: {backup_filename}")
    
    try:
        # Dump database to file
        with open(backup_filename, "w") as f:
            subprocess.run(
                [
                    "pg_dump",
                    f"--host={DB_HOST}",
                    f"--port={DB_PORT}",
                    f"--username={DB_USER}",
                    f"--dbname={DB_NAME}",
                ],
                env={**os.environ, "PGPASSWORD": DB_PASSWORD},
                stdout=f,
                check=True,
            )
        
        file_size = os.path.getsize(backup_filename) / (1024 * 1024)  # MB
        print(f"✅ Database dumped locally: {file_size:.2f} MB")
        
        # Upload to S3
        print(f"📤 Uploading to S3: s3://{S3_BUCKET}/{backup_filename}")
        s3_client.upload_file(
            backup_filename,
            S3_BUCKET,
            backup_filename,
            ExtraArgs={"Metadata": {"backup_time": timestamp}},
        )
        print(f"✅ Backup uploaded successfully!")
        
        # Clean up local file
        os.remove(backup_filename)
        print(f"🧹 Local backup file removed")
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        sys.exit(1)


def restore_database(backup_file=None):
    """Restore database from S3 backup."""
    try:
        if backup_file is None:
            # Get latest backup
            print(f"📋 Listing backups in s3://{S3_BUCKET}/...")
            response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix="stacktutor_db_")
            
            if "Contents" not in response:
                print("❌ No backups found in S3")
                sys.exit(1)
            
            # Get most recent
            latest = max(response["Contents"], key=lambda x: x["LastModified"])
            backup_file = latest["Key"]
            print(f"📥 Using latest backup: {backup_file}")
        
        # Download from S3
        print(f"📥 Downloading from S3: s3://{S3_BUCKET}/{backup_file}")
        s3_client.download_file(S3_BUCKET, backup_file, backup_file)
        print(f"✅ Backup downloaded: {backup_file}")
        
        # Restore to database
        print(f"♻️  Restoring database...")
        with open(backup_file, "r") as f:
            subprocess.run(
                [
                    "psql",
                    f"--host={DB_HOST}",
                    f"--port={DB_PORT}",
                    f"--username={DB_USER}",
                    f"--dbname={DB_NAME}",
                ],
                env={**os.environ, "PGPASSWORD": DB_PASSWORD},
                stdin=f,
                check=True,
            )
        
        print(f"✅ Database restored successfully!")
        
        # Clean up
        os.remove(backup_file)
        print(f"🧹 Local backup file removed")
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        if backup_file and os.path.exists(backup_file):
            os.remove(backup_file)
        sys.exit(1)


def list_backups():
    """List all backups in S3."""
    try:
        print(f"📋 Backups in s3://{S3_BUCKET}/:\n")
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix="stacktutor_db_")
        
        if "Contents" not in response:
            print("No backups found")
            return
        
        for obj in sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True):
            size_mb = obj["Size"] / (1024 * 1024)
            date = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {obj['Key']:40} {size_mb:8.2f} MB  {date}")
        
    except Exception as e:
        print(f"❌ Failed to list backups: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backup_restore.py [backup|restore|list]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        backup_database()
    elif command == "restore":
        restore_database()
    elif command == "list":
        list_backups()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python backup_restore.py [backup|restore|list]")
        sys.exit(1)
