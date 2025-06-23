"""
projects.py

API endpoints for project management.

- Exposes endpoints for creating, listing, viewing, and joining projects.
- Uses dependency injection for DB session and authentication.
- Returns Pydantic schemas (never raw models).
- All endpoints are grouped under `/api/v1/projects/`.

How to use:
- Register this router in `main.py` to enable project endpoints.
- Use Swagger UI to test endpoints live (authorize with JWT).
- Only authenticated users can create or join projects.

To extend:
- Add endpoints for editing, deleting, searching, or filtering projects.
- Add permission checks for project owners/admins.
- Add analytics, comments, updates, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.project import ProjectCreate, ProjectRead
from app.services.project_service import create_project, get_all_projects, get_project_by_id, join_project
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

# --- Create a new project (auth required) ---
@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def api_create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new project.
    - Only authenticated users can create projects.
    - The current user becomes the project owner.
    """
    return create_project(db, project_in, owner_id=current_user.id)

# --- List all projects (public) ---
@router.get("/", response_model=List[ProjectRead])
def api_list_projects(db: Session = Depends(get_db)):
    """
    List all projects.
    - Public endpoint, no authentication required.
    """
    return get_all_projects(db)

# --- Get a single project by ID (public) ---
@router.get("/{project_id}", response_model=ProjectRead)
def api_get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get a single project by its ID.
    - Public endpoint, no authentication required.
    """
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# --- Join a project as a member (auth required) ---
@router.post("/{project_id}/join")
def api_join_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Join a project as a member.
    - Only authenticated users can join projects.
    - The current user is added as a member.
    """
    return join_project(db, user_id=current_user.id, project_id=project_id)