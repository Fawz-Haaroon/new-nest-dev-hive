"""
auth_service.py

Business logic for registration, login, and token management.

- Handles user registration (with password hashing and uniqueness checks)
- Handles user authentication (login with email or username)
- Can be extended for refresh tokens, email verification, etc.
"""

from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.auth import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from fastapi import HTTPException, status
from typing import Optional

def register_user(db: Session, user_in: UserRegister) -> User:
    """
    Register a new user.
    - Checks for unique email and username.
    - Hashes the password before storing.
    - Sets is_active to True and is_verified to False (for email verification).
    """
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        is_active=True,
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(
    db: Session,
    email: Optional[str] = None,
    username: Optional[str] = None,
    password: str = ""
) -> Optional[User]:
    """
    Authenticate a user using either email or username, and verify password.
    - Returns user if credentials are valid, else None.
    """
    user = None
    if email:
        user = db.query(User).filter(User.email == email).first()
    elif username:
        user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def refresh_access_token(db: Session, refresh_token: str) -> str:
    """
    Validate the refresh token and return a new access token.
    """
    payload = decode_token(refresh_token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    # Optionally: check if refresh_token matches user's stored token for extra security
    return create_access_token({"sub": str(user.id)})

def change_user_password(db: Session, user: User, old_password: str, new_password: str):
    """
    Change the user's password after verifying the old password.
    """
    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user

def logout_user(db: Session, user: User):
    """
    Invalidate the user's refresh token (logout).
    """
    user.refresh_token = None
    db.commit()
    db.refresh(user)
    return True
