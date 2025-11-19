# Key SQLAlchemy imports you'll need:
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # This we already have

class User(Base):
    __tablename__ = "users"  # This tells SQLAlchemy what to name the table in the database

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class VocabularyItem(Base):
    __tablename__ = "vocabulary_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False, index=True)  
    review_count = Column(Integer, default=0)    
    saved_at = Column(DateTime, default=datetime.utcnow)
    last_score = Column(Integer, nullable=True)

class Term(Base):
    __tablename__ = "terms"
    
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # devops, networking, security, swe, system_design
    formal_definition = Column(String, nullable=False)
    example = Column(String, nullable=True)
    simple_definition = Column(String, nullable=False)
    why_it_matters = Column(String, nullable=True)  
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)
    user_answer = Column(String, nullable=False)
    score = Column(Integer, nullable=False)  # 0-100
    ai_feedback = Column(String, nullable=True)
    correct_answer = Column(String, nullable=True)
    attempted_at = Column(DateTime, default=datetime.utcnow)

