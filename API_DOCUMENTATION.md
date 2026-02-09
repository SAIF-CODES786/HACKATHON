# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently no authentication required (add JWT/OAuth for production)

---

## Endpoints

### 1. Upload Resumes

**POST** `/upload`

Upload and parse multiple resume files.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with file uploads

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.docx"
```

**Response:**
```json
{
  "success": 2,
  "failed": 0,
  "candidates": [
    {
      "filename": "resume1.pdf",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-234-567-8900",
      "skills": ["Python", "React", "AWS"],
      "education": [
        {
          "degree": "Bachelor of Science in Computer Science",
          "institution": "MIT",
          "year": "2020"
        }
      ],
      "experience": [
        {
          "company": "Tech Corp",
          "position": "Software Engineer",
          "duration": "2020-2023"
        }
      ],
      "years_of_experience": 3.0,
      "certifications": ["AWS Certified Developer"],
      "upload_date": "2024-01-15T10:30:00"
    }
  ],
  "errors": []
}
```

---

### 2. Set Job Description

**POST** `/job-description`

Set job requirements for scoring.

**Request:**
- Content-Type: `application/x-www-form-urlencoded`

```bash
curl -X POST http://localhost:8000/api/job-description \
  -d "description=Looking for a senior software engineer..." \
  -d "required_skills=Python,React,AWS" \
  -d "min_experience=3" \
  -d "max_experience=10"
```

**Response:**
```json
{
  "message": "Job description set successfully",
  "data": {
    "description": "Looking for a senior software engineer...",
    "required_skills": ["Python", "React", "AWS"],
    "min_experience": 3,
    "max_experience": 10
  }
}
```

---

### 3. Score Candidates

**POST** `/score`

Score all uploaded candidates against job description.

**Request:**
```bash
curl -X POST http://localhost:8000/api/score \
  -d "description=Senior Python developer with React experience" \
  -d "required_skills=Python,React,FastAPI" \
  -d "min_experience=3" \
  -d "max_experience=10"
```

**Response:**
```json
{
  "total_candidates": 5,
  "job_description": {
    "description": "Senior Python developer...",
    "required_skills": ["Python", "React", "FastAPI"],
    "min_experience": 3,
    "max_experience": 10
  },
  "candidates": [
    {
      "rank": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "total_score": 87.5,
      "skills_score": 92.3,
      "experience_score": 85.0,
      "education_score": 85.0,
      "certifications_score": 75.0,
      "breakdown": {
        "skills": "92.3 × 0.4 = 36.92",
        "experience": "85.0 × 0.25 = 21.25",
        "education": "85.0 × 0.2 = 17.0",
        "certifications": "75.0 × 0.15 = 11.25"
      },
      "skills": ["Python", "React", "FastAPI", "AWS"],
      "years_of_experience": 5.0
    }
  ]
}
```

---

### 4. Get Rankings

**GET** `/rankings`

Retrieve ranked candidates with optional filtering.

**Query Parameters:**
- `min_score` (optional): Minimum score threshold (0-100)

```bash
curl "http://localhost:8000/api/rankings?min_score=70"
```

**Response:**
```json
{
  "total_candidates": 3,
  "candidates": [...]
}
```

---

### 5. Get Analytics

**GET** `/analytics`

Generate analytics and visualizations.

```bash
curl http://localhost:8000/api/analytics
```

**Response:**
```json
{
  "statistics": {
    "total_candidates": 10,
    "average_score": 72.5,
    "median_score": 75.0,
    "max_score": 95.2,
    "min_score": 45.3,
    "average_experience": 5.2,
    "total_unique_skills": 45,
    "most_common_skills": ["Python", "JavaScript", "React", "AWS", "Docker"]
  },
  "charts": {
    "skill_distribution": "/charts/skill_distribution.png",
    "experience_distribution": "/charts/experience_distribution.png",
    "score_distribution": "/charts/score_distribution.png",
    "top_candidates_comparison": "/charts/top_candidates_comparison.png"
  }
}
```

---

### 6. Export Results

**GET** `/export`

Export ranked candidates to CSV or Excel.

**Query Parameters:**
- `format`: `csv` or `excel` (default: `csv`)

```bash
curl "http://localhost:8000/api/export?format=csv" --output results.csv
```

**Response:**
- File download (CSV or Excel)

---

### 7. Get Candidate Detail

**GET** `/candidate/{candidate_id}`

Get detailed information for a specific candidate.

```bash
curl http://localhost:8000/api/candidate/0
```

**Response:**
```json
{
  "filename": "resume.pdf",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "skills": ["Python", "React", "AWS"],
  "education": [...],
  "experience": [...],
  "years_of_experience": 5.0,
  "certifications": [...],
  "raw_text": "First 1000 characters of resume..."
}
```

---

### 8. Clear Data

**DELETE** `/clear`

Clear all candidate data and job descriptions.

```bash
curl -X DELETE http://localhost:8000/api/clear
```

**Response:**
```json
{
  "message": "All data cleared successfully"
}
```

---

### 9. Health Check

**GET** `/health`

Check API health status.

```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "candidates_count": 5,
  "job_description_set": true
}
```

---

## Scoring Algorithm

### Weights
- **Skills**: 40% - TF-IDF + Cosine Similarity
- **Experience**: 25% - Years normalized to 0-100
- **Education**: 20% - Degree level scoring
- **Certifications**: 15% - Relevance to job description

### Education Scoring
- PhD/Doctorate: 100
- Master's/MBA: 85
- Bachelor's: 70
- Associate: 50
- Diploma: 40
- High School: 20

### Experience Scoring
- Below minimum: Penalized (max 70)
- Within range: Linear scale 70-100
- Above maximum: Slight penalty (max 15% reduction)

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "No candidates uploaded yet"
}
```

### 404 Not Found
```json
{
  "detail": "Candidate not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limits
Currently no rate limiting (add Redis-based limiting for production)

## CORS
Configured for `http://localhost:5173` by default. Update `ALLOWED_ORIGINS` in `.env` for production.

---

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

These interfaces allow you to test all endpoints directly in the browser.
