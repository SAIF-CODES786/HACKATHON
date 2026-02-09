# Sample Resume Data

This directory contains sample resumes for testing the Resume Screening System.

## Files Included

1. **john_doe_resume.pdf** - Senior Software Engineer with 5 years experience
2. **jane_smith_resume.pdf** - Full-Stack Developer with 3 years experience
3. **michael_chen_resume.pdf** - Junior Developer with 1 year experience
4. **sarah_johnson_resume.pdf** - Senior Engineer with 8 years experience
5. **david_williams_resume.pdf** - Mid-level Developer with 4 years experience

## Creating Your Own Test Resumes

To create realistic test resumes:

1. **Use a resume template** (Google Docs, Canva, or Microsoft Word)
2. **Include these sections:**
   - Contact information (name, email, phone)
   - Professional summary
   - Work experience with companies and dates
   - Education with degree and institution
   - Skills (technical and soft skills)
   - Certifications (if applicable)

3. **Export as PDF or DOCX**

4. **Test the parser** by uploading through the UI

## Tips for Best Parsing Results

- Use standard resume formats (chronological or functional)
- Clearly label sections (Experience, Education, Skills, etc.)
- Use bullet points for easy parsing
- Include years in experience (e.g., "2020-2023")
- List skills with commas or bullet points
- Avoid complex layouts or graphics that may confuse the parser

## Sample Job Description

Use `sample_job_description.txt` to test the scoring algorithm. This job description is designed to match well with the sample resumes provided.

## Expected Results

When scoring the sample resumes against the sample job description:

- **john_doe_resume.pdf**: Should score ~85-90 (strong match)
- **jane_smith_resume.pdf**: Should score ~75-80 (good match)
- **sarah_johnson_resume.pdf**: Should score ~80-85 (strong match)
- **david_williams_resume.pdf**: Should score ~70-75 (good match)
- **michael_chen_resume.pdf**: Should score ~60-65 (moderate match)

Note: Actual scores may vary based on the specific content of the resumes.
