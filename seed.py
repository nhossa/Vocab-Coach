"""
Seed all terms from app.data.terms.ALL_TERMS into the database.
Simple, explicit version.
"""

from sqlalchemy import text
from app.database import SessionLocal
from app.models import Term
from app.data.terms import ALL_TERMS


def seed_terms():
    db = SessionLocal()

    # Check if terms already exist - don't truncate if they do!
    existing_count = db.query(Term).count()
    if existing_count > 0:
        print(f"Terms table already has {existing_count} terms. Skipping seed.")
        db.close()
        return

    unique_terms = {}
    dup_count = 0
    for term in ALL_TERMS:
        key = term["term"].strip().lower()
        if key in unique_terms:
            dup_count += 1
            continue
        unique_terms[key] = term

    for term in unique_terms.values():
        db.add(Term(**term))

    db.commit()
    db.close()
    print(f"Inserted {len(unique_terms)} new terms. Skipped {dup_count} duplicates.")
    
if __name__ == "__main__":
    seed_terms()
