"""
Scoring Engine Module
ML-based candidate scoring using TF-IDF and cosine similarity
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List


class ScoringEngine:
    """Score candidates based on job description match"""
    
    # Default scoring weights
    WEIGHTS = {
        'skills': 0.40,      # 40% - Skill matching
        'experience': 0.25,  # 25% - Years of experience
        'education': 0.20,   # 20% - Education level
        'certifications': 0.15  # 15% - Certifications
    }
    
    # Education level scoring
    EDUCATION_SCORES = {
        'phd': 100,
        'doctorate': 100,
        'master': 85,
        'm.tech': 85,
        'm.s': 85,
        'mba': 85,
        'bachelor': 70,
        'b.tech': 70,
        'b.s': 70,
        'associate': 50,
        'diploma': 40,
        'high school': 20
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        """Initialize with custom weights if provided"""
        if weights:
            self.WEIGHTS = weights
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    
    def score_skills(self, candidate_skills: List[str], job_description: str, required_skills: List[str] = None) -> float:
        """
        Score skill matching using TF-IDF and cosine similarity
        Returns score 0-100
        """
        if not candidate_skills:
            return 0.0
        
        # Combine candidate skills into a single text
        candidate_text = ' '.join(candidate_skills)
        
        # Use required skills if provided, otherwise extract from job description
        if required_skills:
            job_text = ' '.join(required_skills) + ' ' + job_description
        else:
            job_text = job_description
        
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([job_text, candidate_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to 0-100 scale
            score = similarity * 100
            
            # Bonus for exact skill matches
            if required_skills:
                candidate_skills_lower = [s.lower() for s in candidate_skills]
                required_skills_lower = [s.lower() for s in required_skills]
                
                matches = sum(1 for skill in required_skills_lower if skill in candidate_skills_lower)
                match_ratio = matches / len(required_skills) if required_skills else 0
                
                # Boost score based on exact matches (up to 20% bonus)
                score = min(100, score + (match_ratio * 20))
            
            return round(score, 2)
        
        except Exception as e:
            print(f"Error in skill scoring: {e}")
            return 0.0
    
    def score_experience(self, years: float, min_years: float = 0, max_years: float = 15) -> float:
        """
        Score years of experience
        Returns score 0-100
        """
        if years <= 0:
            return 0.0
        
        # Normalize years to 0-100 scale
        # Assume optimal experience is between min_years and max_years
        if years < min_years:
            # Penalize for insufficient experience
            score = (years / min_years) * 70  # Max 70 if below minimum
        elif years <= max_years:
            # Ideal range - linear scale
            score = 70 + ((years - min_years) / (max_years - min_years)) * 30
        else:
            # Over-qualified - slight penalty
            score = 100 - min((years - max_years) * 2, 15)  # Max 15% penalty
        
        return round(min(100, max(0, score)), 2)
    
    def score_education(self, education_list: List[Dict[str, str]]) -> float:
        """
        Score education level
        Returns score 0-100
        """
        if not education_list:
            return 0.0
        
        max_score = 0
        
        for edu in education_list:
            degree = edu.get('degree', '').lower()
            
            # Find matching education level
            for level, score in self.EDUCATION_SCORES.items():
                if level in degree:
                    max_score = max(max_score, score)
                    break
        
        return float(max_score)
    
    def score_certifications(self, certifications: List[str], job_description: str) -> float:
        """
        Score certifications based on relevance
        Returns score 0-100
        """
        if not certifications:
            return 0.0
        
        # Base score for having certifications
        base_score = 50
        
        # Check relevance to job description
        job_lower = job_description.lower()
        relevant_count = 0
        
        for cert in certifications:
            cert_lower = cert.lower()
            # Check if certification keywords appear in job description
            cert_words = cert_lower.split()
            if any(word in job_lower for word in cert_words if len(word) > 3):
                relevant_count += 1
        
        # Calculate relevance bonus
        if certifications:
            relevance_ratio = relevant_count / len(certifications)
            relevance_bonus = relevance_ratio * 50
        else:
            relevance_bonus = 0
        
        total_score = base_score + relevance_bonus
        return round(min(100, total_score), 2)
    
    def calculate_overall_score(
        self,
        candidate: Dict,
        job_description: str,
        required_skills: List[str] = None,
        min_experience: float = 0,
        max_experience: float = 15
    ) -> Dict[str, float]:
        """
        Calculate overall weighted score for a candidate
        Returns dict with breakdown and total score
        """
        # Calculate individual scores
        skills_score = self.score_skills(
            candidate.get('skills', []),
            job_description,
            required_skills
        )
        
        experience_score = self.score_experience(
            candidate.get('years_of_experience', 0),
            min_experience,
            max_experience
        )
        
        education_score = self.score_education(
            candidate.get('education', [])
        )
        
        certifications_score = self.score_certifications(
            candidate.get('certifications', []),
            job_description
        )
        
        # Calculate weighted total
        total_score = (
            skills_score * self.WEIGHTS['skills'] +
            experience_score * self.WEIGHTS['experience'] +
            education_score * self.WEIGHTS['education'] +
            certifications_score * self.WEIGHTS['certifications']
        )
        
        return {
            'total_score': round(total_score, 2),
            'skills_score': skills_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'certifications_score': certifications_score,
            'breakdown': {
                'skills': f"{skills_score} × {self.WEIGHTS['skills']} = {round(skills_score * self.WEIGHTS['skills'], 2)}",
                'experience': f"{experience_score} × {self.WEIGHTS['experience']} = {round(experience_score * self.WEIGHTS['experience'], 2)}",
                'education': f"{education_score} × {self.WEIGHTS['education']} = {round(education_score * self.WEIGHTS['education'], 2)}",
                'certifications': f"{certifications_score} × {self.WEIGHTS['certifications']} = {round(certifications_score * self.WEIGHTS['certifications'], 2)}"
            }
        }
    
    def rank_candidates(self, candidates: List[Dict], job_description: str, **kwargs) -> List[Dict]:
        """
        Score and rank all candidates
        Returns sorted list with scores
        """
        scored_candidates = []
        
        for candidate in candidates:
            scores = self.calculate_overall_score(candidate, job_description, **kwargs)
            
            # Add scores to candidate data
            candidate_with_score = {
                **candidate,
                **scores
            }
            
            scored_candidates.append(candidate_with_score)
        
        # Sort by total score (descending)
        scored_candidates.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Add rank
        for i, candidate in enumerate(scored_candidates, 1):
            candidate['rank'] = i
        
        return scored_candidates


# Singleton instance
scoring_engine = ScoringEngine()
