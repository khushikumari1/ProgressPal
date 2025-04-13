from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth import decode_access_token
from .database import SessionLocal
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    # Decode token to get payload
    payload = decode_access_token(token)
    
    # Check if payload is valid
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    # Fetch user based on the 'sub' field in the token (typically user id)
    user = db.query(models.User).filter(models.User.id == payload["sub"]).first()
    
    # If user not found, raise error
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
