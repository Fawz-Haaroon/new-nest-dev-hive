"""
session.py

Database session and engine setup using SQLAlchemy Core.

- Creates a SQLAlchemy engine and session factory.
- Used for all DB access throughout the app.
- No ORM magic—explicit, clear, and easy to debug.

You can import `SessionLocal` and `engine` wherever you need DB access.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# --- SQLAlchemy Engine ---
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

# --- Session Factory ---
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)