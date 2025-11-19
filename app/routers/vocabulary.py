"""
Vocabulary Router - Handles user's saved terms
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import VocabularyItemResponse, VocabularyListResponse
from app.database import get_db
from app.models import VocabularyItem, Term, User
from app.auth.auth_bearer import get_current_user

# Create router instance
router = APIRouter(
    prefix="/vocabulary",
    tags=["vocabulary"]
)


@router.get("/", response_model=VocabularyListResponse)
async def get_vocabulary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all saved vocabulary items for user
    """
    # Get all vocabulary items with their associated terms
    vocab_items = db.query(VocabularyItem).join(Term).all()
    
    # Build response with term details
    items = []
    for item in vocab_items:
        items.append(VocabularyItemResponse(
            id=item.id,
            term=item.term.term,
            category=item.term.category,
            saved_at=item.saved_at,
            review_count=item.review_count,
            last_score=item.last_score
        ))
    
    return VocabularyListResponse(
        items=items,
        total=len(items)
    )


@router.post("/{term_id}")
async def save_term_to_vocabulary(term_id: int, db: Session = Depends(get_db)):
    """
    Save a term to user's vocabulary
    """
    # Check if term exists
    term = db.query(Term).filter(Term.id == term_id).first()
    
    if not term:
        raise HTTPException(
            status_code=404,
            detail=f"Term with id {term_id} not found"
        )
    
    # Create vocabulary item
    vocab_item = VocabularyItem(
        user_id=None,  # Will add after authentication
        term_id=term_id
    )
    
    db.add(vocab_item)
    db.commit()
    
    return {"message": f"Term '{term.term}' saved to vocabulary", "term_id": term_id}
