"""
JWT Bearer token verification for protected routes
"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.auth.auth_handler import decode_jwt
from app.database import get_db
from app.models import User

#This tells FastAPI: "Look for a token in the Authorization header formatted as Bearer <token>"
# Example request header:
# Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# HTTPBearer() automatically extracts the token part after "Bearer ".
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    """
    # Extract token from credentials
    token = credentials.credentials
    
    # Decode JWT to get payload
    payload = decode_jwt(token)
    
    # Check if token is valid
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    
    # Extract user_id from payload
    user_id = payload.get("user_id")
    
    # Query database for user
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    # Check if user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
