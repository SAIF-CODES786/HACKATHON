"""
Advanced NLP Module
Enhanced resume parsing using transformer models
"""

import spacy
from transformers import pipeline
from typing import List, Dict
import re

# Load models
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Initialize transformer pipeline for NER (optional - requires transformers)
try:
    ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
    USE_TRANSFORMERS = True
except:
    USE_TRANSFORMERS = False
    print("Transformers not available, using spaCy only")


class AdvancedNLP:
    """Advanced NLP processing for resume analysis"""
    
    def __init__(self):
        self.nlp = nlp
        self.use_transformers = USE_TRANSFORMERS
    
    def extract_entities_advanced(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using both spaCy and transformers
        Returns: dict with entity types and values
        """
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': [],
            'skills': []
        }
        
        # spaCy NER
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities['persons'].append(ent.text)
            elif ent.label_ == "ORG":
                entities['organizations'].append(ent.text)
            elif ent.label_ == "GPE" or ent.label_ == "LOC":
                entities['locations'].append(ent.text)
            elif ent.label_ == "DATE":
                entities['dates'].append(ent.text)
        
        # Transformer NER (if available)
        if self.use_transformers and len(text) < 5000:  # Limit text length
            try:
                transformer_entities = ner_pipeline(text[:5000])
                for entity in transformer_entities:
                    if entity['entity_group'] == 'PER':
                        entities['persons'].append(entity['word'])
                    elif entity['entity_group'] == 'ORG':
                        entities['organizations'].append(entity['word'])
                    elif entity['entity_group'] == 'LOC':
                        entities['locations'].append(entity['word'])
            except Exception as e:
                print(f"Transformer NER error: {e}")
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def extract_skills_advanced(self, text: str, skill_database: List[str]) -> List[str]:
        """
        Advanced skill extraction using context and patterns
        """
        text_lower = text.lower()
        found_skills = []
        
        # Pattern-based extraction
        skill_patterns = [
            r'skills?:\s*([^\n]+)',
            r'technologies?:\s*([^\n]+)',
            r'proficient in:\s*([^\n]+)',
            r'experience with:\s*([^\n]+)'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                # Split by common separators
                skills = re.split(r'[,;|•]', match)
                for skill in skills:
                    skill = skill.strip()
                    if skill in skill_database:
                        found_skills.append(skill)
        
        # Keyword matching with context
        doc = self.nlp(text)
        for token in doc:
            if token.text.lower() in skill_database:
                # Check if it's used in a skill context
                if any(ancestor.dep_ in ['nsubj', 'dobj', 'pobj'] for ancestor in token.ancestors):
                    found_skills.append(token.text.lower())
        
        return list(set(found_skills))
    
    def calculate_experience_years_advanced(self, text: str) -> float:
        """
        Advanced experience calculation using date parsing
        """
        # Extract all dates
        doc = self.nlp(text)
        years = []
        
        # Find year patterns
        year_pattern = r'\b(19|20)\d{2}\b'
        found_years = re.findall(year_pattern, text)
        years.extend([int(y) for y in found_years])
        
        # Find date ranges
        date_range_pattern = r'(19|20)\d{2}\s*[-–—]\s*(19|20)\d{2}'
        ranges = re.findall(date_range_pattern, text)
        
        total_experience = 0.0
        for start, end in ranges:
            try:
                start_year = int(start + re.search(r'\d{2}', text[text.find(start):text.find(start)+10]).group())
                end_year = int(end + re.search(r'\d{2}', text[text.find(end):text.find(end)+10]).group())
                total_experience += (end_year - start_year)
            except:
                pass
        
        # Fallback: use min/max year difference
        if total_experience == 0 and len(years) >= 2:
            total_experience = max(years) - min(years)
        
        return min(total_experience, 50)  # Cap at 50 years
    
    def extract_education_advanced(self, text: str) -> List[Dict[str, str]]:
        """
        Advanced education extraction with degree classification
        """
        education = []
        
        degree_patterns = {
            'phd': r'(ph\.?d|doctorate|doctoral)',
            'masters': r'(master|m\.s|m\.sc|mba|m\.tech|m\.eng)',
            'bachelors': r'(bachelor|b\.s|b\.sc|b\.tech|b\.eng|b\.a)',
            'associate': r'(associate|a\.s|a\.a)',
        }
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            for degree_type, pattern in degree_patterns.items():
                if re.search(pattern, line_lower):
                    edu_entry = {
                        'degree': line.strip(),
                        'degree_type': degree_type,
                        'institution': '',
                        'year': ''
                    }
                    
                    # Look for institution in nearby lines
                    if i + 1 < len(lines):
                        edu_entry['institution'] = lines[i + 1].strip()
                    
                    # Extract year
                    year_match = re.search(r'\b(19|20)\d{2}\b', line)
                    if year_match:
                        edu_entry['year'] = year_match.group()
                    
                    education.append(edu_entry)
                    break
        
        return education
    
    def sentiment_analysis(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment/tone of resume (professionalism indicator)
        """
        # Simple sentiment based on word choice
        professional_words = ['achieved', 'led', 'managed', 'developed', 'implemented', 'designed']
        casual_words = ['helped', 'did', 'worked', 'tried', 'assisted']
        
        text_lower = text.lower()
        professional_count = sum(1 for word in professional_words if word in text_lower)
        casual_count = sum(1 for word in casual_words if word in text_lower)
        
        total = professional_count + casual_count
        if total == 0:
            return {'professionalism_score': 0.5}
        
        professionalism_score = professional_count / total
        
        return {
            'professionalism_score': round(professionalism_score, 2),
            'professional_words': professional_count,
            'casual_words': casual_count
        }


# Singleton instance
advanced_nlp = AdvancedNLP()
