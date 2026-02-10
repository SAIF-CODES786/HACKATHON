"""
Main FastAPI Application Entry Point
Automated Resume Screening System Backend
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
import logging
from dotenv import load_dotenv
from app.routes import router
from app.database import init_db
from app.exceptions import (
    ResumeParsingError,
    FileSizeExceededError,
    InvalidFileFormatError,
    ScoringEngineError,
    resume_parsing_error_handler,
    file_size_exceeded_handler,
    invalid_file_format_handler,
    scoring_engine_error_handler,
    general_exception_handler
)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Resume Screening System API",
    description="Automated resume parsing, scoring, and ranking system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration - Use explicit origins even in development for security
allowed_origins_str = os.getenv(
    "ALLOWED_ORIGINS", 
    "http://localhost:5173,http://localhost:3000,http://frontend:3000"
)
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request size limiting middleware (10MB max)
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    """Limit request body size to prevent DoS attacks"""
    max_size = 10 * 1024 * 1024  # 10MB
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_size:
            return {"error": "Request body too large", "max_size_mb": 10}
    return await call_next(request)

# Register exception handlers
app.add_exception_handler(ResumeParsingError, resume_parsing_error_handler)
app.add_exception_handler(FileSizeExceededError, file_size_exceeded_handler)
app.add_exception_handler(InvalidFileFormatError, invalid_file_format_handler)
app.add_exception_handler(ScoringEngineError, scoring_engine_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Mount static files for charts
app.mount("/charts", StaticFiles(directory="charts"), name="charts")

# Include API routes
app.include_router(router, prefix="/api")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize resources on application startup"""
    logging.info("Starting Resume Screening System...")
    
    # Initialize database tables
    init_db()
    logging.info("Database initialized")
    
    # Pre-load ML models (spaCy and TF-IDF)
    from app.resume_parser import parser
    from app.scoring_engine import scoring_engine
    
    # Trigger lazy loading of spaCy model
    parser._ensure_nlp_loaded()
    logging.info("spaCy model loaded")
    
    # Initialize TF-IDF vectorizer
    scoring_engine._initialize_vectorizer()
    logging.info("TF-IDF vectorizer initialized")
    
    logging.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on application shutdown"""
    logging.info("Shutting down Resume Screening System...")
    # Add any cleanup logic here (close connections, etc.)
    logging.info("Shutdown complete")

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "online",
        "message": "Resume Screening System API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
