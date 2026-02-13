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
import logging
from functools import wraps
import signal
from app.exceptions import ResumeParsingError, FileSizeExceededError, InvalidFileFormatError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global spaCy model (lazy loaded)
_nlp_model = None

def timeout_handler(signum, frame):
    """Handler for timeout signal"""
    raise TimeoutError("Operation timed out")

def with_timeout(seconds=30):
    """Decorator to add timeout to functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set the signal handler and alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)  # Disable the alarm
            return result
        return wrapper
    return decorator


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
    
    # Pre-compiled regex patterns for performance
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    YEAR_PATTERN = re.compile(r'\b(19|20)\d{2}\b')
    EMAIL_USERNAME_SPLIT = re.compile(r'[._\-\d]+')
    NON_NAME_WORDS = {'with', 'and', 'the', 'for', 'in', 'at', 'to', 'of', 'undergraduate', 'graduate', 'student'}
    
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

    # Common OCR fixes for names (missing first letters)
    COMMON_OCR_FIXES = {
        'umar': 'Kumar',
        'ahul': 'Sahul',
        'ishra': 'Mishra',
        'arma': 'Sharma',
        'upta': 'Gupta',
        'ingh': 'Singh',
        'adav': 'Yadav',
        'riva': 'Srivastava',
        'hane': 'Thane',
        'anwar': 'Tanwar'
    }


    
    def __init__(self):
        # Build comprehensive skill list and set for fast lookups
        self.all_skills = []
        for category_skills in self.SKILLS_DATABASE.values():
            self.all_skills.extend(category_skills)
        
        # Convert to set for O(1) lookups
        self.skills_set = {skill.lower() for skill in self.all_skills}
        
        # Convert forbidden terms to sets for O(1) lookups
        self.forbidden_names_set = {term.lower() for term in self.FORBIDDEN_NAMES}
        self.job_titles_set = {title.lower() for title in self.JOB_TITLES}
        
        # Pre-compile skill patterns for efficient matching
        self._build_skill_pattern()
    
    def _build_skill_pattern(self):
        """Build optimized regex pattern for skill matching"""
        # Sort skills by length (longest first) to match multi-word skills first
        sorted_skills = sorted(self.all_skills, key=len, reverse=True)
        # Escape special regex characters and create pattern
        escaped_skills = [re.escape(skill.lower()) for skill in sorted_skills]
        pattern_str = r'\b(' + '|'.join(escaped_skills) + r')\b'
        self.skills_pattern = re.compile(pattern_str, re.IGNORECASE)
    
    def _ensure_nlp_loaded(self):
        """Lazy load spaCy model on first use"""
        global _nlp_model
        if _nlp_model is None:
            try:
                logger.info("Loading spaCy model...")
                _nlp_model = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded successfully")
            except OSError:
                logger.warning("spaCy model not found, downloading...")
                os.system("python -m spacy download en_core_web_sm")
                _nlp_model = spacy.load("en_core_web_sm")
        return _nlp_model
    
    def _validate_file_size(self, file_path: str, max_size_mb: float = 10) -> None:
        """Validate file size before processing"""
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            raise FileSizeExceededError(file_size_mb, max_size_mb)
    
    @with_timeout(30)
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file with robust error handling"""
        text = ""
        
        # Validate file size first
        try:
            self._validate_file_size(file_path)
        except FileSizeExceededError:
            raise
        
        try:
            with pdfplumber.open(file_path) as pdf:
                # Check if PDF is encrypted
                if pdf.metadata.get('Encrypt'):
                    raise ResumeParsingError(
                        "PDF is password-protected and cannot be processed",
                        filename=os.path.basename(file_path)
                    )
                
                # Extract text from all pages
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                # Check if we extracted any text
                if not text.strip():
                    raise ResumeParsingError(
                        "PDF contains no extractable text (might be scanned image)",
                        filename=os.path.basename(file_path)
                    )
                    
        except pdfplumber.pdfminer.pdfdocument.PDFPasswordIncorrect:
            raise ResumeParsingError(
                "PDF is password-protected",
                filename=os.path.basename(file_path)
            )
        except pdfplumber.pdfminer.pdfparser.PDFSyntaxError:
            raise ResumeParsingError(
                "PDF file is corrupted or invalid",
                filename=os.path.basename(file_path)
            )
        except TimeoutError:
            raise ResumeParsingError(
                "PDF processing timed out (file too complex)",
                filename=os.path.basename(file_path)
            )
        except Exception as e:
            logger.error(f"Unexpected error extracting PDF {file_path}: {str(e)}")
            raise ResumeParsingError(
                f"Failed to extract PDF: {str(e)}",
                filename=os.path.basename(file_path)
            )
        
        return text
    
    @with_timeout(30)
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file with robust error handling"""
        text = ""
        
        # Validate file size first
        try:
            self._validate_file_size(file_path)
        except FileSizeExceededError:
            raise
        
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Check if we extracted any text
            if not text.strip():
                raise ResumeParsingError(
                    "DOCX contains no extractable text",
                    filename=os.path.basename(file_path)
                )
                
        except TimeoutError:
            raise ResumeParsingError(
                "DOCX processing timed out (file too complex)",
                filename=os.path.basename(file_path)
            )
        except Exception as e:
            logger.error(f"Error extracting DOCX {file_path}: {str(e)}")
            raise ResumeParsingError(
                f"Failed to extract DOCX: {str(e)}",
                filename=os.path.basename(file_path)
            )
        
        return text
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address using pre-compiled regex"""
        emails = self.EMAIL_PATTERN.findall(text)
        return emails[0] if emails else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number using pre-compiled regex"""
        phones = self.PHONE_PATTERN.findall(text)
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
            
            # STEP 1: Job Title Blocker - Reject if contains ANY job-related keyword (O(1) set lookup)
            for job_title in self.job_titles_set:
                if job_title in name_lower:
                    return False  # Immediately discard if contains job title
            
            # Check against forbidden names (tech terms) - O(1) set lookup
            for forbidden in self.forbidden_names_set:
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
            if any(word in name_lower for word in self.NON_NAME_WORDS):
                return False
            
            return True

        def clean_and_merge_name(name: str) -> str:
            """Clean name and merge split initials/words"""
            if not name:
                return name
            
            # Remove extra whitespace
            name = ' '.join(name.split())
            
            # Fix split initials like "S K" -> "SK" but preserve "S Kumar" as is
            words = name.split()
            cleaned_words = []
            skip_next = False
            
            for i, word in enumerate(words):
                if skip_next:
                    skip_next = False
                    continue
                
                # Only merge if BOTH current and next are single letters (initials)
                if len(word) == 1 and i + 1 < len(words) and len(words[i + 1]) == 1:
                    # Merge consecutive initials: "S K" -> "SK"
                    cleaned_words.append(word + words[i + 1])
                    skip_next = True  # Skip the next word since we merged it
                else:
                    # Keep the word as is (whether it's a single letter or full word)
                    cleaned_words.append(word)
            
            return ' '.join(cleaned_words)

        
        def extract_name_from_email(email: str) -> str:
            """Extract name from email address as fallback"""
            if not email:
                return "Unknown Candidate"
            
            # Get part before @
            username = email.split('@')[0].lower()
            
            # Remove numbers and special characters
            name_parts = re.split(r'[._\-\d]+', username)
            name_parts = [part.capitalize() for part in name_parts if part and len(part) > 1]
            
            if name_parts:
                # If the first part is very long, it might be concatenated (e.g., "sahulshawlike")
                # We should stop at 2 parts maximum for a name
                return ' '.join(name_parts[:2])
            return username.capitalize()
        
        def fix_name_with_email(extracted_name: str, email: Optional[str]) -> str:
            """
            Cross-reference extracted name with email to fix OCR errors or missing letters
            Example: If PDF has "AHUL" but email is "sahulshaw92@gmail.com", correct to "SAHUL"
            """
            if not extracted_name:
                return extracted_name
            
            # 1. Apply Common OCR Fixes first (e.g., Umar -> Kumar)
            words = extracted_name.lower().split()
            fixed_words = []
            for word in words:
                if word in self.COMMON_OCR_FIXES:
                    fixed_words.append(self.COMMON_OCR_FIXES[word])
                else:
                    fixed_words.append(word.capitalize())
            
            extracted_name = ' '.join(fixed_words)
            
            if not email:
                return extracted_name
            
            # 2. Cross-reference with email handle
            email_name = extract_name_from_email(email)
            email_parts = email_name.lower().split()
            extracted_parts = extracted_name.lower().split()
            
            if not email_parts or not extracted_parts:
                return extracted_name
            
            # Check if extracted name is a missing prefix case (e.g., "ahul" instead of "sahul")
            corrected_parts = []
            for extracted_part in extracted_parts:
                best_match = extracted_part
                found_in_email = False
                for email_part in email_parts:
                    # Find if extracted name exists inside the email handle
                    idx = email_part.find(extracted_part.lower())
                    
                    # If it's a missing prefix case (e.g., "ahul" in "sahulshawlike")
                    # We allow missing 1 or 2 characters at the start.
                    if 1 <= idx <= 2:
                        potential_match = email_part[:idx + len(extracted_part)]
                        logger.info(f"DEBUG: Correcting '{extracted_part}' to '{potential_match}' (missing prefix using email handle)")
                        best_match = potential_match
                        found_in_email = True
                        break
                
                if not found_in_email:
                    # If not in email, but we already fixed it via COMMON_OCR_FIXES, keep it
                    # (best_match is already capitalized correctly if it was in common fixes)
                    corrected_parts.append(best_match.capitalize())
                else:
                    corrected_parts.append(best_match.capitalize())
            
            corrected_name = ' '.join(corrected_parts)
            if corrected_name.lower() != extracted_name.lower():
                logger.info(f"DEBUG: Name corrected from '{extracted_name}' to '{corrected_name}' using email/fixes")
            
            return corrected_name
        
        # Strategy 1: Use spaCy NER to find PERSON entities
        nlp = self._ensure_nlp_loaded()
        doc = nlp(text[:1000])  # Check first 1000 chars (increased from 500)
        
        candidates = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                logger.info(f"DEBUG: spaCy found PERSON entity: '{ent.text}'")
                # Clean and merge the name first
                cleaned_name = clean_and_merge_name(ent.text)
                logger.info(f"DEBUG: After clean_and_merge_name: '{cleaned_name}'")
                
                # Fix name using email if available
                if email:
                    cleaned_name = fix_name_with_email(cleaned_name, email)
                
                if is_valid_name(cleaned_name):
                    # Score based on position (earlier is better) and word count
                    position_score = 1.0 - (ent.start_char / 1000)  # Earlier = higher score
                    word_count = len(cleaned_name.split())
                    word_score = 1.0 if 2 <= word_count <= 4 else 0.5  # Prefer 2-4 words
                    
                    candidates.append({
                        'name': cleaned_name.strip(),
                        'score': position_score + word_score
                    })
                    logger.info(f"DEBUG: Valid candidate added: '{cleaned_name.strip()}' (score: {position_score + word_score})")
                else:
                    logger.info(f"DEBUG: Rejected by is_valid_name: '{cleaned_name}'")
        
        # Return highest scoring candidate
        if candidates:
            best_candidate = max(candidates, key=lambda x: x['score'])
            logger.info(f"DEBUG: Best candidate selected: '{best_candidate['name']}'")
            return best_candidate['name']
        
        # Strategy 2: Check first few lines for name-like patterns
        logger.info("DEBUG: Strategy 1 (spaCy) failed, trying Strategy 2 (first lines)")
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for i, line in enumerate(lines[:5]):  # Check first 5 non-empty lines
            logger.info(f"DEBUG: Strategy 2 - Checking line {i}: '{line[:100]}'")
            # Skip lines that are clearly not names
            if len(line) > 50 or '@' in line or 'http' in line.lower():
                logger.info(f"DEBUG: Strategy 2 - Skipped line {i} (too long or contains @ or http)")
                continue
            
            # Clean and merge the line
            cleaned_line = clean_and_merge_name(line)
            logger.info(f"DEBUG: Strategy 2 - After cleaning: '{cleaned_line}'")
            
            if is_valid_name(cleaned_line):
                # Additional check: should have at least one space for first+last name
                if ' ' in cleaned_line:
                    logger.info(f"DEBUG: Strategy 2 - Found valid name: '{cleaned_line}'")
                    # Fix name using email if available
                    if email:
                        cleaned_line = fix_name_with_email(cleaned_line, email)
                        logger.info(f"DEBUG: Strategy 2 - After email fix: '{cleaned_line}'")
                    return cleaned_line
                else:
                    logger.info(f"DEBUG: Strategy 2 - Rejected '{cleaned_line}' (no space)")
        
        # Strategy 3: Extract from email if available
        logger.info("DEBUG: Strategy 2 failed, trying Strategy 3 (email extraction)")
        if email:
            extracted = extract_name_from_email(email)
            logger.info(f"DEBUG: Strategy 3 - Extracted from email '{email}': '{extracted}'")
            return extracted
        
        # Strategy 4: Try to extract email from text and use it
        extracted_email = self.extract_email(text)
        if extracted_email:
            return extract_name_from_email(extracted_email)
        
        # Final fallback
        return "Unknown Candidate"


    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills using optimized pattern matching"""
        # Use pre-compiled pattern for all skills at once
        matches = self.skills_pattern.findall(text.lower())
        
        # Convert to title case and remove duplicates
        found_skills = {match.title() for match in matches}
        
        return list(found_skills)
    
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
                
                # Try to find year (4 digits) using pre-compiled pattern
                year_match = self.YEAR_PATTERN.search(line)
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
        nlp = self._ensure_nlp_loaded()
        doc = nlp(text)
        
        # Find organizations (companies) and persons (to filter out)
        person_names = {ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"}
        companies = []
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Don't use person names as company names
                if ent.text.lower() not in person_names:
                    # Also check if it's not a substring of a person name
                    is_person_name = False
                    for person in person_names:
                        if ent.text.lower() in person or person in ent.text.lower():
                            is_person_name = True
                            break
                    
                    if not is_person_name:
                        companies.append(ent.text)
        
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
        """Calculate total years of experience using pre-compiled pattern"""
        # Find all years mentioned using pre-compiled pattern
        years = self.YEAR_PATTERN.findall(text)
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
