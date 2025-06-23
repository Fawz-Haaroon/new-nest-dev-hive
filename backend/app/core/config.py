"""
config.py

Centralized configuration for the backend.

- Loads environment variables and settings.
- Provides a single `settings` object for use throughout the app.
- Uses Pydantic for validation and type safety.

Add new settings here as needed (e.g., DB URL, JWT secret, etc).
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/nestdevhive"
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    # JWT
    JWT_SECRET_KEY: str = "supersecretkey"  # Change in production!
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Singleton settings object
settings = Settings()