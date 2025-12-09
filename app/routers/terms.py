"""
Terms Router - Handles term explanation/lookup
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas import TermRequest, TermResponse, TermSuggestRequest, TermSuggestResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Term, User
from app.auth.auth_bearer import get_current_user
from app.services.ai_client import validate_and_generate_term
from zoneinfo import ZoneInfo
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)

# Create router instance
router = APIRouter(
    prefix="/terms",
    tags=["terms"]
)

#output validation through TermResponse
@router.post("/", response_model=TermResponse)
async def explain_term(
    request: TermRequest,
    current_user: User = Depends(get_current_user),
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
        id=term.id,
        term=term.term,
        formal_definition=term.formal_definition,
        simple_definition=term.simple_definition,
        example=term.example,
        why_it_matters=term.why_it_matters,
        category=term.category,
        category_id=term.category_id,
        difficulty=term.difficulty,
        created_at=term.created_at,
    )


@router.get("/all", response_model=list[TermResponse])
async def get_all_terms(
    current_user: User = Depends(get_current_user),
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Get all terms, optionally filtered by category
    """
    query = db.query(Term)
    
    # Filter by category if provided
    if category:
        query = query.filter(Term.category == category)
    
    # Get all terms, ordered by term name
    terms = query.order_by(Term.term).all()
    
    return [
        TermResponse(
            id=term.id,
            term=term.term,
            formal_definition=term.formal_definition,
            simple_definition=term.simple_definition,
            example=term.example,
            why_it_matters=term.why_it_matters,
            category=term.category,
            category_id=term.category_id,
            difficulty=term.difficulty,
            created_at=term.created_at,
        )
        for term in terms
    ]


@router.get("/{term_id}", response_model=TermResponse)
async def get_term_by_id(
    term_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific term by ID
    """
    term = db.query(Term).filter(Term.id == term_id).first()
    
    if not term:
        raise HTTPException(
            status_code=404,
            detail=f"Term with ID {term_id} not found"
        )
    
    return TermResponse(
        id=term.id,
        term=term.term,
        formal_definition=term.formal_definition,
        simple_definition=term.simple_definition,
        example=term.example,
        why_it_matters=term.why_it_matters,
        category=term.category,
        category_id=term.category_id,
        difficulty=term.difficulty,
        created_at=term.created_at,
    )


@router.post("/suggest", response_model=TermSuggestResponse)
@limiter.limit("1/minute", error_message="Slow down! You can only suggest 1 term per minute. This helps prevent spam and gives our AI time to validate each suggestion properly.")
async def suggest_new_term(
    request: Request,
    term_request: TermSuggestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User suggests a new term. AI validates and generates content if approved.
    Rate limited to 1 suggestion per minute to prevent spam.
    """
    # Normalize the input term for comparison (lowercase, remove periods, extra spaces)
    normalized_input = term_request.term.lower().strip().rstrip('.').replace('  ', ' ')
    
    # Check for exact duplicates first (case-insensitive, ignoring punctuation)
    existing_terms = db.query(Term).all()
    for existing in existing_terms:
        normalized_existing = existing.term.lower().strip().rstrip('.').replace('  ', ' ')
        if normalized_input == normalized_existing:
            return TermSuggestResponse(
                approved=False,
                reason=f"This term already exists in our database as '{existing.term}'",
                term_data=None
            )
    
    # Get all existing terms for AI validation
    existing_term_names = [t.term for t in existing_terms]
    
    # Use AI to validate and generate content
    ai_result = validate_and_generate_term(term_request.term, existing_term_names)
    
    if not ai_result:
        raise HTTPException(
            status_code=500,
            detail="AI validation service failed"
        )
    
    # If rejected, return the reason
    if not ai_result.get("approved"):
        return TermSuggestResponse(
            approved=False,
            reason=ai_result.get("reason", "Term was rejected"),
            term_data=None
        )
    
    # If approved, create new term in database
    new_term = Term(
        term=term_request.term,
        formal_definition=ai_result.get("formal_definition"),
        simple_definition=ai_result.get("simple_definition"),
        example=ai_result.get("example"),
        why_it_matters=ai_result.get("why_it_matters"),
        category=ai_result.get("category"),
        difficulty=ai_result.get("difficulty"),
        created_at=datetime.now(ZoneInfo("UTC"))
    )
    
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    
    # Return success with term data
    return TermSuggestResponse(
        approved=True,
        reason=ai_result.get("reason", "Term approved and added!"),
        term_data=TermResponse(
            id=new_term.id,
            term=new_term.term,
            formal_definition=new_term.formal_definition,
            simple_definition=new_term.simple_definition,
            example=new_term.example,
            why_it_matters=new_term.why_it_matters,
            category=new_term.category,
            category_id=new_term.category_id,
            difficulty=new_term.difficulty,
            created_at=new_term.created_at
        )
    )