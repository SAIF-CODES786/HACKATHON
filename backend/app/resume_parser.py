"""
Resume Parser Module
Extracts structured information from PDF and DOCX resumes
"""

import re
import pdfplumber
from docx import Document
import spacy
from typing import Dict, List, Optional
import os

# Load spaCy model for NLP
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


class ResumeParser:
    """Parse resumes and extract structured information"""
    
    # Common skill keywords (expandable)
    SKILLS_DATABASE = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin', 'typescript'],
        'web': ['react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'html', 'css', 'tailwind'],
        'data': ['sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'pandas', 'numpy', 'spark'],
        'ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'nlp', 'computer vision'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
        'tools': ['git', 'jira', 'agile', 'scrum', 'rest api', 'graphql', 'microservices']
    }
    
    EDUCATION_KEYWORDS = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'b.s', 'm.s', 'mba', 'degree', 'university', 'college']
    CERTIFICATION_KEYWORDS = ['certified', 'certification', 'certificate', 'aws', 'azure', 'google cloud', 'pmp', 'cissp']
    
    # Forbidden names - common tech terms that should never be names
    FORBIDDEN_NAMES = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin',
        # Libraries & Frameworks
        'react', 'angular', 'vue', 'node', 'nodejs', 'express', 'django', 'flask', 'fastapi', 'spring',
        'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly', 'tensorflow', 'pytorch', 'keras',
        # Tools & Platforms
        'docker', 'kubernetes', 'git', 'github', 'gitlab', 'jenkins', 'aws', 'azure', 'gcp',
        'linux', 'windows', 'macos', 'ubuntu', 'debian',
        # Design Tools
        'adobe', 'photoshop', 'illustrator', 'figma', 'sketch', 'xd',
        # Databases
        'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'sql',
        # Other Tech Terms
        'api', 'rest', 'graphql', 'microservices', 'devops', 'agile', 'scrum', 'jira'
    ]
    
    # Job titles - common job-related keywords that should never be in names
    JOB_TITLES = [
        'developer', 'engineer', 'manager', 'associate', 'consultant', 'analyst', 
        'intern', 'designer', 'architect', 'lead', 'senior', 'junior', 'staff',
        'principal', 'director', 'head', 'chief', 'officer', 'specialist',
        'stack', 'frontend', 'backend', 'fullstack', 'full-stack', 'full stack',
        'software', 'data', 'web', 'mobile', 'cloud', 'security', 'network',
        'product', 'project', 'program', 'technical', 'tech', 'it', 'qa', 'qe',
        'coordinator', 'administrator', 'executive', 'assistant', 'representative'
    ]


    
    def __init__(self):
        self.all_skills = []
        for category_skills in self.SKILLS_DATABASE.values():
            self.all_skills.extend(category_skills)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number using regex"""
        # Matches various phone formats
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def extract_name(self, text: str, email: Optional[str] = None) -> Optional[str]:
        """
        Extract name using NLP with validation and fallback mechanisms
        
        Args:
            text: Resume text
            email: Email address (for fallback)
            
        Returns:
            Validated candidate name or fallback
        """
        def is_valid_name(name: str) -> bool:
            """Validate if extracted text is a reasonable name"""
            if not name:
                return False
            
            name = name.strip()
            
            # Check length (names should be < 50 characters)
            if len(name) > 50:
                return False
            
            name_lower = name.lower()
            
            # STEP 1: Job Title Blocker - Reject if contains ANY job-related keyword
            for job_title in self.JOB_TITLES:
                if job_title in name_lower:
                    return False  # Immediately discard if contains job title
            
            # Check against forbidden names (tech terms)
            for forbidden in self.FORBIDDEN_NAMES:
                if forbidden in name_lower:
                    return False
            
            # STEP 2: Word Count Limit - Real names rarely exceed 4 words
            words = name.split()
            if len(words) < 2:  # Must have at least first + last name
                return False
            if len(words) > 4:  # Maximum 4 words (e.g., "Mary Jane O'Connor Smith")
                return False
            
            # Check if it's mostly alphabetic (allow spaces, hyphens, apostrophes)
            alpha_chars = sum(c.isalpha() or c.isspace() or c in ['-', "'", '.'] for c in name)
            if alpha_chars / len(name) < 0.8:  # At least 80% should be valid name characters
                return False
            
            # Reject if it looks like a sentence (contains common non-name words)
            non_name_words = ['with', 'and', 'the', 'for', 'in', 'at', 'to', 'of', 'undergraduate', 'graduate', 'student']
            if any(word in name_lower for word in non_name_words):
                return False
            
            return True


        
        def extract_name_from_email(email: str) -> str:
            """Extract name from email address as fallback"""
            if not email:
                return "Unknown Candidate"
            
            # Get part before @
            username = email.split('@')[0]
            
            # Remove numbers and special characters
            name_parts = re.split(r'[._\-\d]+', username)
            name_parts = [part.capitalize() for part in name_parts if part and len(part) > 1]
            
            if name_parts:
                return ' '.join(name_parts[:2])  # Take first two parts (first name, last name)
            return username.capitalize()
        
        # Strategy 1: Use spaCy NER to find PERSON entities
        doc = nlp(text[:1000])  # Check first 1000 chars (increased from 500)
        
        candidates = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if is_valid_name(ent.text):
                    # Score based on position (earlier is better) and word count
                    position_score = 1.0 - (ent.start_char / 1000)  # Earlier = higher score
                    word_count = len(ent.text.split())
                    word_score = 1.0 if 2 <= word_count <= 4 else 0.5  # Prefer 2-4 words
                    
                    candidates.append({
                        'name': ent.text.strip(),
                        'score': position_score + word_score
                    })
        
        # Return highest scoring candidate
        if candidates:
            best_candidate = max(candidates, key=lambda x: x['score'])
            return best_candidate['name']
        
        # Strategy 2: Check first few lines for name-like patterns
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:5]:  # Check first 5 non-empty lines
            # Skip lines that are clearly not names
            if len(line) > 50 or '@' in line or 'http' in line.lower():
                continue
            
            if is_valid_name(line):
                # Additional check: should have at least one space for first+last name
                if ' ' in line:
                    return line
        
        # Strategy 3: Extract from email if available
        if email:
            return extract_name_from_email(email)
        
        # Strategy 4: Try to extract email from text and use it
        extracted_email = self.extract_email(text)
        if extracted_email:
            return extract_name_from_email(extracted_email)
        
        # Final fallback
        return "Unknown Candidate"

    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills by keyword matching"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Check if line contains education keywords
            if any(keyword in line_lower for keyword in self.EDUCATION_KEYWORDS):
                edu_entry = {
                    'degree': line.strip(),
                    'institution': '',
                    'year': ''
                }
                
                # Try to find year (4 digits)
                year_match = re.search(r'\b(19|20)\d{2}\b', line)
                if year_match:
                    edu_entry['year'] = year_match.group()
                
                # Look at next line for institution
                if i + 1 < len(lines):
                    edu_entry['institution'] = lines[i + 1].strip()
                
                education.append(edu_entry)
        
        return education
    
    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience"""
        experience = []
        
        # Look for common job title patterns and company names
        doc = nlp(text)
        
        # Find organizations (companies)
        companies = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        # Extract years of experience (rough estimate)
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        
        if companies:
            for company in companies[:5]:  # Limit to 5 companies
                exp_entry = {
                    'company': company,
                    'position': 'Not specified',
                    'duration': ''
                }
                experience.append(exp_entry)
        
        return experience
    
    def calculate_years_of_experience(self, text: str) -> float:
        """Calculate total years of experience"""
        # Find all years mentioned
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        if len(years) >= 2:
            years_int = [int(y) for y in years]
            # Estimate: difference between oldest and newest year
            return max(years_int) - min(years_int)
        return 0.0
    
    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        text_lower = text.lower()
        
        for keyword in self.CERTIFICATION_KEYWORDS:
            if keyword in text_lower:
                # Find the line containing the certification
                for line in text.split('\n'):
                    if keyword in line.lower():
                        certifications.append(line.strip())
                        break
        
        return list(set(certifications))
    
    def parse_resume(self, file_path: str, filename: str) -> Dict:
        """Main parsing function - orchestrates all extraction"""
        # Determine file type and extract text
        if filename.lower().endswith('.pdf'):
            text = self.extract_text_from_pdf(file_path)
        elif filename.lower().endswith('.docx'):
            text = self.extract_text_from_docx(file_path)
        else:
            return {"error": "Unsupported file format"}
        
        if not text:
            return {"error": "Could not extract text from file"}
        
        # Extract email first (needed for name fallback)
        email = self.extract_email(text)
        
        # Extract all information
        parsed_data = {
            'filename': filename,
            'name': self.extract_name(text, email),  # Pass email for fallback
            'email': email,
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'education': self.extract_education(text),
            'experience': self.extract_experience(text),
            'years_of_experience': self.calculate_years_of_experience(text),
            'certifications': self.extract_certifications(text),
            'raw_text': text[:1000]  # Store first 1000 chars for reference
        }
        
        return parsed_data


# Singleton instance
parser = ResumeParser()
