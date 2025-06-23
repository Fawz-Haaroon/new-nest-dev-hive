"""
user.py

Pydantic schemas for User.

- Used for request validation and response serialization.
- Never expose sensitive fields (like hashed_password) in public schemas.
- Includes schemas for user creation, reading, updating, and public profile.
"""

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    Shared properties for User (used in many places).
    """
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """
    Properties required to create a new user.
    """
    password: str  # Plain password (will be hashed)

class UserRead(UserBase):
    """
    Properties returned to the client (never include password).
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility

class UserInDB(UserBase):
    """
    Internal schema for DB (includes hashed_password).
    """
    id: int
    hashed_password: str
    created_at: datetime

class UserProfileUpdate(BaseModel):
    """
    Properties that can be updated in a user's profile.
    """
    username: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None

class UserPublic(BaseModel):
    """
    Public user profile schema (for self and others).
    """
    id: int
    email: EmailStr
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True