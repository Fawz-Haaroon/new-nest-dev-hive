"""
auth.py

API endpoints for authentication flows:
- /register: Register a new user (email, username, password)
- /login: Authenticate user and return JWT access & refresh tokens
- /refresh: Exchange a valid refresh token for a new access token
- /change-password: Change the current user's password (requires authentication)
- /logout: Log out the current user (invalidate refresh token)

How to use:
- Register and login users via Swagger UI or frontend.
- Use the "Authorize" button in Swagger UI to test protected endpoints.
- Extend with email verification, password reset, etc. as needed.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.auth import (
    UserRegister, UserLogin, Token, UserPublic,
    RefreshTokenRequest, ChangePasswordRequest
)
from app.services.auth_service import (
    register_user, authenticate_user, refresh_access_token,
    change_user_password, logout_user
)
from app.core.security import create_access_token, create_refresh_token
from app.api.v1.dependencies import get_current_user
from app.db.models import User

router = APIRouter()

# --- Dependency to get DB session ---
def get_db():
    """
    Yields a database session for use in endpoints.
    Ensures the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Register a new user ---
@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def api_register(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Checks for unique email and username.
    - Hashes password before storing.
    - Returns public user info (never password).
    """
    user = register_user(db, user_in)
    return user

# --- Login and get JWT tokens ---
@router.post("/login", response_model=Token)
def api_login(user_in: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access & refresh tokens.
    - Returns 401 if credentials are invalid.
    """
    user = authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token)

# --- Refresh token endpoint ---
@router.post("/refresh", response_model=Token)
def api_refresh_token(
    token_in: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Exchange a valid refresh token for a new access token.
    """
    access_token = refresh_access_token(db, token_in.refresh_token)
    return Token(access_token=access_token, refresh_token=token_in.refresh_token)

# --- Change password endpoint ---
@router.post("/change-password", response_model=UserPublic)
def api_change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change the current user's password (requires authentication).
    - Verifies old password before updating.
    """
    user = change_user_password(db, current_user, req.old_password, req.new_password)
    return user

# --- Logout endpoint ---
@router.post("/logout")
def api_logout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Log out the current user (invalidate refresh token).
    """
    logout_user(db, current_user)
    return {"detail": "Logged out successfully"}

@router.post("/logout")
def api_logout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Log out the current user (invalidate refresh token).
    """
    logout_user(db, current_user)
    return {"detail": "Logged out successfully"}