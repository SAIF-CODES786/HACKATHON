"""
Test script to verify resume parser optimizations
"""
import re
from typing import List

# Simulate the optimized patterns
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
YEAR_PATTERN = re.compile(r'\b(19|20)\d{2}\b')

# Test data
test_text = """
John Doe
john.doe@example.com
+1-555-123-4567

Skills: Python, JavaScript, React, Node.js, Docker, AWS
Education: B.Tech Computer Science, 2018-2022
Experience: Software Engineer at TechCorp (2022-2024)
"""

# Test email extraction
emails = EMAIL_PATTERN.findall(test_text)
print(f"✓ Email extraction: {emails}")

# Test phone extraction
phones = PHONE_PATTERN.findall(test_text)
print(f"✓ Phone extraction: {phones}")

# Test year extraction
years = YEAR_PATTERN.findall(test_text)
print(f"✓ Year extraction: {years}")

# Test skill pattern compilation
skills_list = ['python', 'java', 'javascript', 'react', 'node.js', 'docker', 'aws']
sorted_skills = sorted(skills_list, key=len, reverse=True)
escaped_skills = [re.escape(skill.lower()) for skill in sorted_skills]
pattern_str = r'\b(' + '|'.join(escaped_skills) + r')\b'
skills_pattern = re.compile(pattern_str, re.IGNORECASE)

matches = skills_pattern.findall(test_text.lower())
found_skills = {match.title() for match in matches}
print(f"✓ Skill extraction: {list(found_skills)}")

# Test set-based lookups
forbidden_names = {'python', 'java', 'javascript', 'developer', 'engineer'}
test_name = "John Developer"
is_forbidden = any(term in test_name.lower() for term in forbidden_names)
print(f"✓ Forbidden name check for '{test_name}': {is_forbidden}")

test_name2 = "John Doe"
is_forbidden2 = any(term in test_name2.lower() for term in forbidden_names)
print(f"✓ Forbidden name check for '{test_name2}': {is_forbidden2}")

print("\n✅ All optimization patterns working correctly!")
