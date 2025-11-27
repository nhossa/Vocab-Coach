"""
Quiz Router - Handles quiz generation and answer grading
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from zoneinfo import ZoneInfo

from app.schemas import QuizQuestion, QuizAnswerRequest, QuizResult
from app.database import get_db
from app.models import Term, QuizAttempt, User
from app.auth.auth_bearer import get_current_user
from app.services.ai_client import grade_user_answer
from typing import Optional


# Create router instance
router = APIRouter(
    prefix="/quiz",
    tags=["quiz"]
)



@router.get("/random", response_model=QuizQuestion)
async def get_random_quiz(
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a random term to quiz on, optionally filtered by category and difficulty
    """
    query = db.query(Term)
    if category:
        query = query.filter(Term.category == category)
    if difficulty:
        query = query.filter(Term.difficulty == difficulty)
    random_term = query.order_by(func.random()).first()
    if not random_term:
        raise HTTPException(
            status_code=404,
            detail="No terms available in database for the given filters."
        )
    return QuizQuestion(
        term_id=random_term.id,
        term=f"Explain {random_term.term}",
        category=random_term.category,
        difficulty=random_term.difficulty
    )


@router.post("/answer", response_model=QuizResult)
async def submit_answer(
    answer: QuizAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit quiz answer and get AI grading
    """
    # Get the term from database
    term = db.query(Term).filter(Term.id == answer.term_id).first()
    
    if not term:
        raise HTTPException(
            status_code=404,
            detail=f"Term with id {answer.term_id} not found"
        )
    
    ai_result = grade_user_answer(term.term, term.simple_definition, answer.user_answer)
    print(f"DEBUG: AI grader result: {ai_result}")

    if not ai_result or "score" not in ai_result or "feedback" not in ai_result:
        raise HTTPException(
            status_code=500,
            detail="AI grader failed to return a valid score and feedback. Please check server logs."
        )

    score = ai_result.get("score")
    ai_feedback = ai_result.get("feedback")
    # Save quiz attempt to database
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        term_id=answer.term_id,
        user_answer=answer.user_answer,
        score=score,
        ai_feedback=ai_feedback,
        correct_answer=term.simple_definition
    )
    
    db.add(quiz_attempt)
    db.commit()

    

    # If this term is weak for you, save to vocabulary (if not already saved)
    from app.models import VocabularyItem
    saved_to_vocabulary = score < 70
    if saved_to_vocabulary:
        existing_vocab = db.query(VocabularyItem).filter(
            VocabularyItem.user_id == current_user.id,
            VocabularyItem.term_id == answer.term_id
        ).first()
        if not existing_vocab:
            vocab_item = VocabularyItem(
                user_id=current_user.id,
                term_id=answer.term_id,
                review_count=0,
                saved_at=datetime.now(),
                last_score=score
            )
            db.add(vocab_item)
            db.commit()


    return QuizResult(
        term=term.term,
        score=score,
        feedback=ai_feedback,
        correct_answer=term.simple_definition,
        your_answer=answer.user_answer,
        saved_to_vocabulary=saved_to_vocabulary
    )