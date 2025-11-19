"""
Terms Router - Handles term explanation/lookup
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TermRequest, TermResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Term
from zoneinfo import ZoneInfo

# Create router instance
router = APIRouter(
    prefix="/api/v1/terms",
    tags=["terms"]
)


@router.post("/", response_model=TermResponse)
async def explain_term(
    request: TermRequest,
    db: Session = Depends(get_db)
):
    """
    Explain a technical term
    """
    # Query database for the term
    term = db.query(Term).filter(Term.term.ilike(request.term)).first()
    
    if not term:
        raise HTTPException(
            status_code=404,
            detail=f"Term '{request.term}' not found in database"
        )
    
    return TermResponse(
    term=term.term,
    formal_definition=term.formal_definition,
    simple_definition=term.simple_definition,
    examples=[term.example] if term.example else [],
    why_it_matters=term.why_it_matters or "No information available",
    category=term.category,
    timestamp=datetime.now(ZoneInfo("UTC"))
)