"""
models.py

Defines all database models using SQLAlchemy ORM.

- User: Represents a user account.
- Project: Represents a collaborative project.
- ProjectMember: Join table for users and projects (team membership).

This is the single source of truth for your database schema.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, ARRAY, func
from sqlalchemy.orm import declarative_base, relationship

# --- SQLAlchemy Declarative Base ---
Base = declarative_base()

class User(Base):
    """
    User model/table definition.

    - id: Primary key, auto-incrementing integer
    - email: Unique email address
    - username: Unique username
    - hashed_password: Hashed password (never store plain text!)
    - is_active: Is the user allowed to log in?
    - is_verified: Has the user verified their email? (for email verification)
    - refresh_token: Stores the latest refresh token (for refresh token flow)
    - created_at: Timestamp of user creation
    - projects: Projects owned by this user
    - project_memberships: Projects this user is a member of
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # Can the user log in?
    is_verified = Column(Boolean, default=False)  # Has the user verified their email?
    refresh_token = Column(String, nullable=True)  # For refresh token flow (optional)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    projects = relationship("Project", back_populates="owner")
    project_memberships = relationship("ProjectMember", back_populates="user")

class Project(Base):
    """
    Project model/table definition.

    - id: Primary key
    - title: Project title
    - short_description: Brief summary
    - detailed_description: Full description
    - difficulty: Difficulty level (e.g., beginner, intermediate, advanced)
    - status: Open/closed
    - max_team_members: Team size limit
    - tags: List of tags (e.g., 'React', 'Analytics')
    - tech_stack: List of technologies used
    - repository_url: GitHub or other repo link
    - live_demo_url: Live demo link
    - created_at: Timestamp
    - owner_id: Foreign key to User
    - owner: Relationship to User
    - members: List of ProjectMember objects (team members)
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    detailed_description = Column(Text)
    difficulty = Column(String, nullable=False)
    status = Column(String, default="open")
    max_team_members = Column(Integer, default=5)
    tags = Column(ARRAY(String))
    tech_stack = Column(ARRAY(String))
    repository_url = Column(String)
    live_demo_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="projects")
    members = relationship("ProjectMember", back_populates="project")

class ProjectMember(Base):
    """
    ProjectMember model/table definition.

    - id: Primary key
    - user_id: Foreign key to User
    - project_id: Foreign key to Project
    - role: Role in the project (e.g., 'owner', 'member')
    - joined_at: Timestamp
    - user: Relationship to User
    - project: Relationship to Project
    """
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role = Column(String, default="member")
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="project_memberships")
    project = relationship("Project", back_populates="members")