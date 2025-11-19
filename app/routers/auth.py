"""
Authentication Router - Handles user registration and login
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import UserLogin, UserRegister
from app.database import get_db
from app.models import User
from app.auth.auth_handler import sign_jwt
from app.auth.auth_utils import hash_password, verify_password


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login user
    """
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return sign_jwt(str(existing_user.id))


@router.post("/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create the User object id automaticallly generates because it's primary key
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    # Add to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Get the auto-generated id

    # Return JWT token
    return sign_jwt(str(new_user.id))
