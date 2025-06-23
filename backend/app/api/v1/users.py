"""
users.py

User API endpoints (CRUD + profile).

- Exposes endpoints for creating, listing, and updating users.
- Uses dependency injection for DB session and authentication.
- Returns Pydantic schemas (never raw models).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserRead, UserProfileUpdate, UserPublic
from app.services.user_service import create_user, get_all_users, get_user_by_id, update_user_profile
from app.api.v1.dependencies import get_current_user
from app.db.models import User

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def api_create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    try:
        user = create_user(db, user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserRead])
def api_list_users(db: Session = Depends(get_db)):
    """
    List all users.
    """
    return get_all_users(db)

@router.get("/me", response_model=UserPublic)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile (requires authentication).
    """
    return current_user

@router.put("/me", response_model=UserPublic)
def update_my_profile(
    update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the current user's profile (requires authentication).
    """
    user = update_user_profile(db, current_user, update.dict(exclude_unset=True))
    return user

@router.get("/{user_id}", response_model=UserPublic)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Get a public user profile by user ID.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user