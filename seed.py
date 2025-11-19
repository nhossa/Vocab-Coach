"""
Add sample terms to database
"""
from app.database import SessionLocal
from app.models import Term

def seed_terms():
    """Add sample terms to database"""
    db = SessionLocal()
    
    terms_data = [
        {
            "term": "Docker",
            "category": "devops",
            "formal_definition": "An open platform for developing, shipping, and running applications using containerization.",
            "simple_definition": "A tool that packages your app into a portable container.",
            "example": "Run the same code on your laptop and production server.",
            "why_it_matters": "Solves 'works on my machine' problem. Used by 99% of companies."
        },
        {
            "term": "Load Balancer",
            "category": "networking",
            "formal_definition": "A device or software that distributes network traffic across multiple servers to ensure no single server is overwhelmed.",
            "simple_definition": "A traffic cop for your servers - sends requests to different servers to balance the work.",
            "example": "AWS Elastic Load Balancer distributes traffic across 10 EC2 instances.",
            "why_it_matters": "Prevents server crashes during high traffic and enables horizontal scaling."
        },
        {
            "term": "CI/CD",
            "category": "devops",
            "formal_definition": "Continuous Integration/Continuous Deployment - automated practices for testing and deploying code changes.",
            "simple_definition": "Automatically test and deploy your code when you push to GitHub.",
            "example": "GitHub Actions runs tests on every commit and deploys to production if tests pass.",
            "why_it_matters": "Reduces manual errors, speeds up releases, and catches bugs early."
        },
        {
            "term": "API",
            "category": "backend",
            "formal_definition": "Application Programming Interface - a set of rules and protocols for building and interacting with software applications.",
            "simple_definition": "A menu of actions your software can perform that other software can request.",
            "example": "GET /users/123 returns data about user 123 in JSON format.",
            "why_it_matters": "Enables different systems to communicate - the backbone of modern web apps."
        }
    ]
    
    added_count = 0
    skipped_count = 0
    
    for term_data in terms_data:
        # Check if term already exists (case-insensitive)
        existing = db.query(Term).filter(Term.term.ilike(term_data["term"])).first()
        
        if existing:
            print(f"⏭️  Skipped '{term_data['term']}' - already exists")
            skipped_count += 1
        else:
            new_term = Term(**term_data)
            db.add(new_term)
            added_count += 1
            print(f"✅ Added '{term_data['term']}'")
    
    db.commit()
    print(f"\n📊 Summary: Added {added_count}, Skipped {skipped_count}")
    db.close()


if __name__ == "__main__":
    seed_terms()