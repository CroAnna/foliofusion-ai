from jose import jwt, JWTError
import os
from fastapi import HTTPException

def verify_jwt(token: str):
    """
    Verify JWT token and return payload if valid
    """
    try:
        SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        return payload
    except JWTError as e:
        print("JWT verification failed:", e)
        return None

def get_and_validate_current_user(auth_header: str):
    """
    Extract and validate token from authorization header
    """
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = auth_header.split(" ")[1]
    user = verify_jwt(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user