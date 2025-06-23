"""
project.py

Pydantic schemas for Project and ProjectMember.

- Used for request validation and response serialization in the API.
- Ensures all data sent to and from the API is type-checked and validated.
- These schemas are the contract between frontend and backend for project-related data.

How to use:
- Use `ProjectCreate` for POST requests to create a new project.
- Use `ProjectRead` for responses (never include sensitive/internal fields).
- Use `ProjectMemberRead` for team membership info.

To extend:
- Add new fields to the schemas as your features grow.
- Use Pydantic validators for custom validation logic.
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# --- Base schema for shared project fields ---
class ProjectBase(BaseModel):
    title: str
    short_description: str
    detailed_description: Optional[str] = None
    difficulty: str
    status: Optional[str] = "open"
    max_team_members: int = 5
    tags: List[str] = []
    tech_stack: List[str] = []
    repository_url: Optional[HttpUrl] = None
    live_demo_url: Optional[HttpUrl] = None

# --- Schema for creating a new project (request body) ---
class ProjectCreate(ProjectBase):
    pass

# --- Schema for reading project data (response) ---
class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model

# --- Schema for reading project member data ---
class ProjectMemberRead(BaseModel):
    id: int
    user_id: int
    project_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True