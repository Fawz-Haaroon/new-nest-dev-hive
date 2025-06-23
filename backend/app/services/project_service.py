"""
project_service.py

Business logic for project operations.

- Handles project creation, retrieval, and team membership.
- Interacts with the database session and models.
- Keeps API endpoints clean by separating business rules from HTTP logic.

How to use:
- Call these functions from your API endpoints to perform project-related actions.
- Pass in the database session and any required parameters.

To extend:
- Add more functions for editing, deleting, searching, or filtering projects.
- Add permission checks, notifications, or analytics as needed.
"""

from sqlalchemy.orm import Session
from app.db.models import Project, ProjectMember
from app.schemas.project import ProjectCreate

# --- Create a new project and add the owner as the first member ---
def create_project(db: Session, project_in: ProjectCreate, owner_id: int) -> Project:
    # Convert HttpUrl fields to str for SQLAlchemy/psycopg2
    data = project_in.dict()
    if data.get("repository_url") is not None:
        data["repository_url"] = str(data["repository_url"])
    if data.get("live_demo_url") is not None:
        data["live_demo_url"] = str(data["live_demo_url"])
    project = Project(**data, owner_id=owner_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    # Add owner as first member
    member = ProjectMember(user_id=owner_id, project_id=project.id, role="owner")
    db.add(member)
    db.commit()
    return project

# --- Retrieve all projects from the database ---
def get_all_projects(db: Session):
    return db.query(Project).all()

# --- Retrieve a single project by its ID ---
def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

# --- Add a user as a member to a project (if not already a member) ---
def join_project(db: Session, user_id: int, project_id: int):
    # Check if already a member
    existing = db.query(ProjectMember).filter_by(user_id=user_id, project_id=project_id).first()
    if existing:
        return existing
    member = ProjectMember(user_id=user_id, project_id=project_id)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

