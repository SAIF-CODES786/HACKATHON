"""
Database Models
SQLAlchemy models for persistent storage
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from contextlib import contextmanager
from typing import Generator
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://resume_user:resume_password@postgres:5432/resume_screening"
)

# Create engine with connection pooling for production
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Number of connections to maintain
    max_overflow=20,        # Max additional connections
    pool_pre_ping=True,     # Verify connections before using
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=False              # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Candidate(Base):
    """Candidate model for storing parsed resume data"""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    skills = Column(JSON)  # List of skills
    education = Column(JSON)  # List of education entries
    experience = Column(JSON)  # List of experience entries
    years_of_experience = Column(Float, default=0.0)
    certifications = Column(JSON)  # List of certifications
    raw_text = Column(Text)
    
    # Scoring fields
    total_score = Column(Float, default=0.0)
    skills_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    certifications_score = Column(Float, default=0.0)
    rank = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    job_description_id = Column(Integer, index=True)


class JobDescription(Base):
    """Job description model"""
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(JSON)
    min_experience = Column(Float, default=0.0)
    max_experience = Column(Float, default=15.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)  # User ID when auth is implemented


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Integer, default=1)
    is_admin = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)



# Context manager for database sessions with automatic transaction handling
@contextmanager
def get_db_context() -> Generator:
    """
    Provides a transactional scope for database operations
    Automatically commits on success, rolls back on error, and closes session
    
    Usage:
        with get_db_context() as db:
            db.add(candidate)
            # Automatically commits here
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db() -> Generator:
    """
    FastAPI dependency for database sessions
    Use with Depends() in route parameters
    
    Usage:
        @router.get("/candidates")
        def get_candidates(db: Session = Depends(get_db)):
            return db.query(Candidate).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

