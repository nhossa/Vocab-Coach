"""
Pydantic Schemas - API Request/Response Models
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# ============================================
# AUTH SCHEMAS
# ============================================

class UserRegister(BaseModel):
    """User registration - input"""
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    """User login - input"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token - output"""
    access_token: str
    token_type: str = "bearer"


# ============================================
# TERM SCHEMAS (Explain endpoint)
# ============================================

class TermRequest(BaseModel):
    """Request to explain a term"""
    term: str = Field(min_length=1, max_length=100)


class TermResponse(BaseModel):
    """Response with term explanation"""
    term: str
    formal_definition: str
    simple_definition: str
    examples: List[str]
    why_it_matters: str
    category: str
    timestamp: datetime


# ============================================
# QUIZ SCHEMAS
# ============================================

class QuizQuestion(BaseModel):
    """Random quiz question - output"""
    term_id: int
    term: str


class QuizAnswerRequest(BaseModel):
    """User's answer submission - input"""
    term_id: int
    user_answer: str = Field(min_length=10)


class QuizResult(BaseModel):
    """Quiz result with AI feedback - output"""
    score: int = Field(ge=0, le=100)  # Between 0-100
    feedback: str
    correct_answer: str
    saved_to_vocabulary: bool


# ============================================
# VOCABULARY SCHEMAS
# ============================================

class VocabularyItemResponse(BaseModel):
    """Single vocabulary item - output"""
    id: int
    term: str
    category: str
    saved_at: datetime
    review_count: int
    last_score: Optional[int]


class VocabularyListResponse(BaseModel):
    """User's full vocabulary list - output"""
    items: List[VocabularyItemResponse]
    total: int