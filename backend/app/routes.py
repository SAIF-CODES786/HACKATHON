"""
API Routes
FastAPI endpoints for resume screening system
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import shutil
import json
from datetime import datetime
import pandas as pd

from .resume_parser import parser
from .scoring_engine import scoring_engine
from .analytics import analytics

router = APIRouter()

# In-memory storage (replace with database in production)
candidates_db = []
job_description_db = {"description": "", "required_skills": []}


@router.post("/upload")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Upload and parse multiple resumes
    Returns parsed candidate data
    """
    parsed_candidates = []
    errors = []
    
    for file in files:
        # Validate file type
        if not (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
            errors.append(f"{file.filename}: Unsupported file type")
            continue
        
        # Save file temporarily
        upload_path = os.path.join("uploads", file.filename)
        try:
            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Parse resume
            parsed_data = parser.parse_resume(upload_path, file.filename)
            
            if "error" in parsed_data:
                errors.append(f"{file.filename}: {parsed_data['error']}")
            else:
                parsed_data['upload_date'] = datetime.now().isoformat()
                parsed_candidates.append(parsed_data)
                candidates_db.append(parsed_data)
        
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
        
        finally:
            # Clean up uploaded file
            if os.path.exists(upload_path):
                os.remove(upload_path)
    
    return {
        "success": len(parsed_candidates),
        "failed": len(errors),
        "candidates": parsed_candidates,
        "errors": errors
    }


@router.post("/job-description")
async def set_job_description(
    description: str = Form(...),
    required_skills: Optional[str] = Form(None),
    min_experience: Optional[float] = Form(0),
    max_experience: Optional[float] = Form(15)
):
    """
    Set job description and requirements for scoring
    """
    skills_list = []
    if required_skills:
        skills_list = [s.strip() for s in required_skills.split(',')]
    
    job_description_db.update({
        "description": description,
        "required_skills": skills_list,
        "min_experience": min_experience,
        "max_experience": max_experience
    })
    
    return {
        "message": "Job description set successfully",
        "data": job_description_db
    }


@router.post("/score")
async def score_candidates(
    description: str = Form(...),
    required_skills: Optional[str] = Form(None),
    min_experience: Optional[float] = Form(0),
    max_experience: Optional[float] = Form(15)
):
    """
    Score all candidates against job description
    Returns ranked candidates with scores
    """
    if not candidates_db:
        raise HTTPException(status_code=400, detail="No candidates uploaded yet")
    
    # Parse required skills
    skills_list = []
    if required_skills:
        skills_list = [s.strip() for s in required_skills.split(',')]
    
    # Update job description
    job_description_db.update({
        "description": description,
        "required_skills": skills_list,
        "min_experience": min_experience,
        "max_experience": max_experience
    })
    
    # Score and rank candidates
    ranked_candidates = scoring_engine.rank_candidates(
        candidates_db,
        description,
        required_skills=skills_list if skills_list else None,
        min_experience=min_experience,
        max_experience=max_experience
    )
    
    return {
        "total_candidates": len(ranked_candidates),
        "job_description": job_description_db,
        "candidates": ranked_candidates
    }


@router.get("/rankings")
async def get_rankings(min_score: Optional[float] = 0):
    """
    Get ranked candidates (optionally filtered by minimum score)
    """
    if not candidates_db:
        return {"candidates": []}
    
    # Re-score with current job description
    if job_description_db.get("description"):
        ranked = scoring_engine.rank_candidates(
            candidates_db,
            job_description_db["description"],
            required_skills=job_description_db.get("required_skills"),
            min_experience=job_description_db.get("min_experience", 0),
            max_experience=job_description_db.get("max_experience", 15)
        )
    else:
        ranked = candidates_db
    
    # Filter by minimum score
    if min_score > 0:
        ranked = [c for c in ranked if c.get('total_score', 0) >= min_score]
    
    return {
        "total_candidates": len(ranked),
        "candidates": ranked
    }


@router.get("/analytics")
async def get_analytics():
    """
    Generate analytics and visualizations
    Returns chart URLs and summary statistics
    """
    if not candidates_db:
        raise HTTPException(status_code=400, detail="No candidates uploaded yet")
    
    # Generate charts
    charts = analytics.generate_all_analytics(candidates_db)
    
    # Get summary statistics
    stats = analytics.get_summary_statistics(candidates_db)
    
    # Convert file paths to URLs
    chart_urls = {}
    for chart_name, filepath in charts.items():
        # Extract filename from path
        filename = os.path.basename(filepath)
        chart_urls[chart_name] = f"/charts/{filename}"
    
    return {
        "statistics": stats,
        "charts": chart_urls
    }


@router.get("/export")
async def export_results(format: str = "csv"):
    """
    Export ranked candidates to CSV or Excel
    """
    if not candidates_db:
        raise HTTPException(status_code=400, detail="No candidates uploaded yet")
    
    # Re-score with current job description
    if job_description_db.get("description"):
        ranked = scoring_engine.rank_candidates(
            candidates_db,
            job_description_db["description"],
            required_skills=job_description_db.get("required_skills"),
            min_experience=job_description_db.get("min_experience", 0),
            max_experience=job_description_db.get("max_experience", 15)
        )
    else:
        ranked = candidates_db
    
    # Prepare data for export
    export_data = []
    for candidate in ranked:
        export_data.append({
            'Rank': candidate.get('rank', 'N/A'),
            'Name': candidate.get('name', 'Unknown'),
            'Email': candidate.get('email', 'N/A'),
            'Phone': candidate.get('phone', 'N/A'),
            'Total Score': candidate.get('total_score', 0),
            'Skills Score': candidate.get('skills_score', 0),
            'Experience Score': candidate.get('experience_score', 0),
            'Education Score': candidate.get('education_score', 0),
            'Certifications Score': candidate.get('certifications_score', 0),
            'Years of Experience': candidate.get('years_of_experience', 0),
            'Skills': ', '.join(candidate.get('skills', [])),
            'Certifications': ', '.join(candidate.get('certifications', []))
        })
    
    # Create DataFrame
    df = pd.DataFrame(export_data)
    
    # Export based on format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format.lower() == "excel":
        filename = f"candidates_ranked_{timestamp}.xlsx"
        filepath = os.path.join("exports", filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
    else:
        filename = f"candidates_ranked_{timestamp}.csv"
        filepath = os.path.join("exports", filename)
        df.to_csv(filepath, index=False)
    
    return FileResponse(
        filepath,
        media_type='application/octet-stream',
        filename=filename
    )


@router.get("/candidate/{candidate_id}")
async def get_candidate_detail(candidate_id: int):
    """
    Get detailed information for a specific candidate
    """
    if candidate_id < 0 or candidate_id >= len(candidates_db):
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidates_db[candidate_id]


@router.delete("/clear")
async def clear_data():
    """
    Clear all candidate data (for testing)
    """
    candidates_db.clear()
    job_description_db.update({
        "description": "",
        "required_skills": []
    })
    
    return {"message": "All data cleared successfully"}


@router.get("/health")
async def health_check():
    """
    API health check
    """
    return {
        "status": "healthy",
        "candidates_count": len(candidates_db),
        "job_description_set": bool(job_description_db.get("description"))
    }
