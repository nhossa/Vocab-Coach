"""
Add sample terms to database
"""

from app.database import SessionLocal
from app.models import Term
from terms_data_200 import terms_data_200

def seed_terms():
    """Add sample terms to database"""
    db = SessionLocal()
    terms_data = terms_data_200
    
    added_count = 0
    skipped_count = 0
    
    seen_terms = set()
    for term_data in terms_data:
        term_lower = term_data["term"].strip().lower()
        if term_lower in seen_terms:
            print(f"  Skipped '{term_data['term']}' - duplicate in input list")
            skipped_count += 1
            continue
        seen_terms.add(term_lower)
        # Check if term already exists (case-insensitive)
        existing = db.query(Term).filter(Term.term.ilike(term_data["term"])).first()
        if existing:
            print(f"  Skipped '{term_data['term']}' - already exists in DB")
            skipped_count += 1
        else:
            new_term = Term(**term_data)
            db.add(new_term)
            added_count += 1
            print(f"Added '{term_data['term']}'")
    
    db.commit()
    print(f"\n Summary: Added {added_count}, Skipped {skipped_count}")
    db.close()


if __name__ == "__main__":
    seed_terms()