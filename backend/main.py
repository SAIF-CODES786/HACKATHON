"""
Main FastAPI Application Entry Point
Automated Resume Screening System Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv
from app.routes import router

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

# CORS Configuration
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://frontend:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# Allow all origins in development
if os.getenv("DEBUG", "True") == "True":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Mount static files for charts
app.mount("/charts", StaticFiles(directory="charts"), name="charts")

# Include API routes
app.include_router(router, prefix="/api")

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
