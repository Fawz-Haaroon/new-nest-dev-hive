"""
main.py

Entrypoint for the FastAPI backend application.

- Creates the FastAPI app instance.
- Includes all API routers (REST and WebSocket).
- Sets up CORS, middleware, and event handlers.
- This is the file you run to start the backend server.

To run locally:
    uvicorn app.main:app --reload

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from app.api.v1 import users as users_api
from app.api.v1 import auth as auth_api
from app.api.ws import presence as ws_presence
from app.api.v1 import projects as projects_api

# Import settings
from app.core.config import settings

# Create FastAPI app instance
app = FastAPI(
    title="new-nest-dev-hive Backend",
    description="Backend API for new-nest-dev-hive, built with FastAPI.",
    version="1.0.0"
)

# --- CORS Middleware Setup ---
# Allow frontend (localhost:5173 for Vite) and docs access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
# REST API endpoints
app.include_router(users_api.router, prefix="/api/v1/users", tags=["users"])
# Auth endpoints (to be implemented)
# Register auth_api.router
app.include_router(auth_api.router, prefix="/api/v1/auth", tags=["auth"])
# WebSocket endpoints
app.include_router(ws_presence.router, prefix="/ws", tags=["websocket"])


app.include_router(projects_api.router, prefix="/api/v1/projects", tags=["projects"])

# --- Event Handlers (optional) ---
# @app.on_event("startup")
# async def startup_event():
#     # TODO: Add startup logic (e.g., connect to DB, Redis)
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
#     # TODO: Add shutdown logic (e.g., close DB, Redis)
#     pass

# --- Root Endpoint ---
@app.get("/")
def read_root():
    """
    Health check endpoint.
    """
    return {"message": "Welcome to the new-nest-dev-hive backend!"}