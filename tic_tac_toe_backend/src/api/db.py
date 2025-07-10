import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load .env if present (used for db config)
load_dotenv()

# Get database url from environment variable (example: 'sqlite:///./test.db' or 'postgresql://user:pass@localhost/db')
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tic_tac_toe.db")  # TODO: Update to match deployment

# Setup SQLAlchemy engine and session factory
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PUBLIC_INTERFACE
def get_db() -> Session:
    """Yield a SQLAlchemy session for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PUBLIC_INTERFACE
def init_db():
    """Create all tables (intended for CLI/init usage, not for runtime)"""
    from .models import Base
    Base.metadata.create_all(bind=engine)
