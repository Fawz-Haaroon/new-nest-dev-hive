"""
auth.py

Pydantic schemas for authentication flows:
- Registration
- Login
- Token responses
- User response (public)
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str