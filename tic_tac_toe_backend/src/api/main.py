from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import DB setup for initialization
from . import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """
    Initialize the database (create tables if not present)

    Notes:
     - In production, use alembic for migrations instead of auto-create.
     - Relies on DATABASE_URL env var, defaulting to local sqlite if unset.
    """
    db.init_db()

@app.get("/")
def health_check():
    """Health check endpoint for the Tic Tac Toe API backend."""
    return {"message": "Healthy"}
