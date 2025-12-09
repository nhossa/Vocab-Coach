"""
JWT token handler for encoding and decoding tokens
"""
import time
from typing import Dict
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")


def token_response(token: str):
    """
    Format token into response dictionary
    """
    return {
        "access_token": token
    }


def sign_jwt(user_id: str) -> Dict[str, str]:
    """
    Create a JWT token for a user
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + 1800  # Token expires in 30 minutes
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token_response(token)


def decode_jwt(token: str) -> dict:
    """
    Decode and verify a JWT token
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        #compares future time to current time to see if token expired
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
