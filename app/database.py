"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL - SQLite file will be created in project root
DATABASE_URL = "sqlite:///./vocab.db"

# Create database engine
# connect_args is only needed for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class - each instance is a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()


# Dependency function to get database session
def get_db():
    """
    Provides a database session to endpoints
    Automatically closes the session when done
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
