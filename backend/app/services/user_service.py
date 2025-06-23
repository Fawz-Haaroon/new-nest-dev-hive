"""
user_service.py

Business logic for user operations.

- Handles user creation, retrieval, update, and (later) delete.
- Interacts with the database session and models.
- Handles password hashing and uniqueness checks.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import User
from app.schemas.user import UserCreate, UserProfileUpdate
from app.core.security import hash_password

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database.

    - Hashes the password before storing.
    - Checks for unique email/username (raises on conflict).
    """
    hashed_pw = hash_password(user_in.password)
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_pw
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email or username already exists.")

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve a user by email.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieve a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session) -> list[User]:
    """
    Retrieve all users.
    """
    return db.query(User).all()

def update_user_profile(db: Session, user: User, update_data: dict) -> User:
    """
    Update the current user's profile with provided fields.
    """
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user