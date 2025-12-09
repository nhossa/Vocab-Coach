"""
Script to find and remove duplicate terms from the database.
Run this to clean up any duplicate terms that slipped through.
"""
import sys
sys.path.append('/app')

from app.database import SessionLocal
from app.models import Term
from sqlalchemy import func

def normalize_term(term: str) -> str:
    """Normalize term for comparison"""
    return term.lower().strip().rstrip('.').replace('  ', ' ')

def find_and_remove_duplicates():
    db = SessionLocal()
    
    try:
        # Get all terms
        all_terms = db.query(Term).all()
        
        # Group by normalized term
        term_groups = {}
        for term in all_terms:
            normalized = normalize_term(term.term)
            if normalized not in term_groups:
                term_groups[normalized] = []
            term_groups[normalized].append(term)
        
        # Find duplicates
        duplicates_found = 0
        for normalized, terms in term_groups.items():
            if len(terms) > 1:
                print(f"\n Found {len(terms)} duplicates for: '{normalized}'")
                
                # Keep the oldest one (lowest ID)
                terms_sorted = sorted(terms, key=lambda t: t.id)
                keep_term = terms_sorted[0]
                delete_terms = terms_sorted[1:]
                
                print(f"    KEEPING: ID={keep_term.id}, '{keep_term.term}'")
                
                for term in delete_terms:
                    print(f"   DELETING: ID={term.id}, '{term.term}'")
                    db.delete(term)
                    duplicates_found += 1
        
        if duplicates_found > 0:
            db.commit()
            print(f"\n Removed {duplicates_found} duplicate term(s)")
        else:
            print("\n No duplicates found!")
            
    except Exception as e:
        print(f" Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔍 Checking for duplicate terms...")
    find_and_remove_duplicates()
