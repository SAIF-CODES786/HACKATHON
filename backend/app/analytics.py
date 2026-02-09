"""
Analytics Module
Generate data visualizations and analytics for candidate pool
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from typing import List, Dict
import os
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


class Analytics:
    """Generate analytics and visualizations for candidate data"""
    
    def __init__(self, output_dir: str = "charts"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_skill_distribution(self, candidates: List[Dict]) -> str:
        """Generate bar chart of most common skills"""
        all_skills = []
        for candidate in candidates:
            all_skills.extend(candidate.get('skills', []))
        
        if not all_skills:
            return None
        
        # Count skill frequency
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(15)
        
        # Create chart
        plt.figure(figsize=(12, 6))
        skills, counts = zip(*top_skills)
        
        bars = plt.bar(range(len(skills)), counts, color='#6366f1')
        plt.xlabel('Skills', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Candidates', fontsize=12, fontweight='bold')
        plt.title('Top 15 Skills in Candidate Pool', fontsize=14, fontweight='bold')
        plt.xticks(range(len(skills)), skills, rotation=45, ha='right')
        plt.tight_layout()
        
        # Save
        filepath = os.path.join(self.output_dir, 'skill_distribution.png')
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_experience_distribution(self, candidates: List[Dict]) -> str:
        """Generate pie chart of experience levels"""
        experience_levels = {
            'Entry (0-2 years)': 0,
            'Junior (2-5 years)': 0,
            'Mid (5-8 years)': 0,
            'Senior (8-12 years)': 0,
            'Expert (12+ years)': 0
        }
        
        for candidate in candidates:
            years = candidate.get('years_of_experience', 0)
            if years <= 2:
                experience_levels['Entry (0-2 years)'] += 1
            elif years <= 5:
                experience_levels['Junior (2-5 years)'] += 1
            elif years <= 8:
                experience_levels['Mid (5-8 years)'] += 1
            elif years <= 12:
                experience_levels['Senior (8-12 years)'] += 1
            else:
                experience_levels['Expert (12+ years)'] += 1
        
        # Filter out zero values
        labels = [k for k, v in experience_levels.items() if v > 0]
        sizes = [v for v in experience_levels.values() if v > 0]
        
        if not sizes:
            return None
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6']
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Experience Level Distribution', fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        # Save
        filepath = os.path.join(self.output_dir, 'experience_distribution.png')
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_score_distribution(self, candidates: List[Dict]) -> str:
        """Generate histogram of candidate scores"""
        scores = [c.get('total_score', 0) for c in candidates]
        
        if not scores:
            return None
        
        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=20, color='#6366f1', edgecolor='black', alpha=0.7)
        plt.xlabel('Total Score', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Candidates', fontsize=12, fontweight='bold')
        plt.title('Candidate Score Distribution', fontsize=14, fontweight='bold')
        plt.axvline(np.mean(scores), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(scores):.1f}')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        # Save
        filepath = os.path.join(self.output_dir, 'score_distribution.png')
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_top_candidates_comparison(self, candidates: List[Dict], top_n: int = 5) -> str:
        """Generate comparison chart for top N candidates"""
        # Get top candidates
        top_candidates = sorted(candidates, key=lambda x: x.get('total_score', 0), reverse=True)[:top_n]
        
        if not top_candidates:
            return None
        
        # Prepare data
        names = [c.get('name', 'Unknown')[:20] for c in top_candidates]
        skills_scores = [c.get('skills_score', 0) for c in top_candidates]
        exp_scores = [c.get('experience_score', 0) for c in top_candidates]
        edu_scores = [c.get('education_score', 0) for c in top_candidates]
        cert_scores = [c.get('certifications_score', 0) for c in top_candidates]
        
        # Create grouped bar chart
        x = np.arange(len(names))
        width = 0.2
        
        plt.figure(figsize=(14, 6))
        plt.bar(x - 1.5*width, skills_scores, width, label='Skills', color='#6366f1')
        plt.bar(x - 0.5*width, exp_scores, width, label='Experience', color='#10b981')
        plt.bar(x + 0.5*width, edu_scores, width, label='Education', color='#f59e0b')
        plt.bar(x + 1.5*width, cert_scores, width, label='Certifications', color='#8b5cf6')
        
        plt.xlabel('Candidates', fontsize=12, fontweight='bold')
        plt.ylabel('Score', fontsize=12, fontweight='bold')
        plt.title(f'Top {top_n} Candidates - Score Breakdown', fontsize=14, fontweight='bold')
        plt.xticks(x, names, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        
        # Save
        filepath = os.path.join(self.output_dir, 'top_candidates_comparison.png')
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def generate_all_analytics(self, candidates: List[Dict]) -> Dict[str, str]:
        """Generate all analytics charts"""
        charts = {}
        
        skill_chart = self.generate_skill_distribution(candidates)
        if skill_chart:
            charts['skill_distribution'] = skill_chart
        
        exp_chart = self.generate_experience_distribution(candidates)
        if exp_chart:
            charts['experience_distribution'] = exp_chart
        
        score_chart = self.generate_score_distribution(candidates)
        if score_chart:
            charts['score_distribution'] = score_chart
        
        comparison_chart = self.generate_top_candidates_comparison(candidates)
        if comparison_chart:
            charts['top_candidates_comparison'] = comparison_chart
        
        return charts
    
    def get_summary_statistics(self, candidates: List[Dict]) -> Dict:
        """Calculate summary statistics"""
        if not candidates:
            return {}
        
        scores = [c.get('total_score', 0) for c in candidates]
        experience_years = [c.get('years_of_experience', 0) for c in candidates]
        
        all_skills = []
        for c in candidates:
            all_skills.extend(c.get('skills', []))
        
        return {
            'total_candidates': len(candidates),
            'average_score': round(np.mean(scores), 2) if scores else 0,
            'median_score': round(np.median(scores), 2) if scores else 0,
            'max_score': round(max(scores), 2) if scores else 0,
            'min_score': round(min(scores), 2) if scores else 0,
            'average_experience': round(np.mean(experience_years), 2) if experience_years else 0,
            'total_unique_skills': len(set(all_skills)),
            'most_common_skills': [skill for skill, _ in Counter(all_skills).most_common(10)]
        }


# Singleton instance
analytics = Analytics()
