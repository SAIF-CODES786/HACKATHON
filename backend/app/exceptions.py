"""
Custom Exception Classes
Provides structured error handling for the Resume Screening System
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict


class ResumeParsingError(HTTPException):
    """Raised when resume parsing fails"""
    def __init__(self, detail: str, filename: str = None):
        self.filename = filename
        super().__init__(status_code=400, detail=detail)


class FileSizeExceededError(HTTPException):
    """Raised when uploaded file exceeds size limit"""
    def __init__(self, size_mb: float, max_size_mb: float = 10):
        detail = f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
        super().__init__(status_code=413, detail=detail)


class InvalidFileFormatError(HTTPException):
    """Raised when file format is not supported"""
    def __init__(self, filename: str, allowed_formats: list = None):
        if allowed_formats is None:
            allowed_formats = ['pdf', 'docx']
        detail = f"File '{filename}' has unsupported format. Allowed formats: {', '.join(allowed_formats)}"
        super().__init__(status_code=415, detail=detail)


class ScoringEngineError(HTTPException):
    """Raised when ML scoring fails"""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Scoring engine error: {detail}")


class DatabaseError(HTTPException):
    """Raised when database operations fail"""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=f"Database error: {detail}")


# Global exception handlers
async def resume_parsing_error_handler(request: Request, exc: ResumeParsingError) -> JSONResponse:
    """Handle resume parsing errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Resume Parsing Failed",
            "detail": exc.detail,
            "filename": exc.filename,
            "type": "parsing_error"
        }
    )


async def file_size_exceeded_handler(request: Request, exc: FileSizeExceededError) -> JSONResponse:
    """Handle file size exceeded errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "File Too Large",
            "detail": exc.detail,
            "type": "file_size_error"
        }
    )


async def invalid_file_format_handler(request: Request, exc: InvalidFileFormatError) -> JSONResponse:
    """Handle invalid file format errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Invalid File Format",
            "detail": exc.detail,
            "type": "format_error"
        }
    )


async def scoring_engine_error_handler(request: Request, exc: ScoringEngineError) -> JSONResponse:
    """Handle scoring engine errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Scoring Failed",
            "detail": exc.detail,
            "type": "scoring_error"
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all unhandled exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
            "type": "server_error"
        }
    )
