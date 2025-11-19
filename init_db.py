"""
Initialize the database - creates all tables
"""
from app.database import engine, Base
from app.models import User, VocabularyItem, Term, QuizAttempt

def init_db():
    """Create all database tables"""
    print("🔨 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print(f"   - {User.__tablename__}")
    print(f"   - {VocabularyItem.__tablename__}")
    print(f"   - {Term.__tablename__}")
    print(f"   - {QuizAttempt.__tablename__}")

if __name__ == "__main__":
    init_db()
