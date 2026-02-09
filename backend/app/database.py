"""
Database Models
SQLAlchemy models for persistent storage
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_screening.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
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


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
