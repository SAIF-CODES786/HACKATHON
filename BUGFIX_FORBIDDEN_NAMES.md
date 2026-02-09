# 🐛 Bug Fix: Skills Being Extracted as Names

## Issue
The resume parser was incorrectly identifying tech skills as candidate names:
- ❌ "Seaborn" extracted as name
- ❌ "Adobe XD" extracted as name  
- ❌ "Python" extracted as name

## Root Cause
The `extract_name()` function didn't filter out tech-related terms that spaCy sometimes tags as `PERSON` entities.

## Solution Applied

### 1. Added FORBIDDEN_NAMES List
Created a comprehensive list of tech terms that should never be names:

```python
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
```

### 2. Enhanced Validation in `is_valid_name()`

**Added forbidden name check:**
```python
# Check against forbidden names (tech terms)
name_lower = name.lower()
for forbidden in self.FORBIDDEN_NAMES:
    if forbidden in name_lower:
        return False  # Reject if contains any tech term
```

**Enforced 2+ word requirement:**
```python
# Require at least 2 words (First Name + Last Name)
words = name.split()
if len(words) < 2:  # Must have first + last name
    return False
```

## Changes Made

### File: `backend/app/resume_parser.py`

**Lines 40-58**: Added `FORBIDDEN_NAMES` constant with 50+ tech terms

**Lines 93-129**: Updated `is_valid_name()` function:
- Check if name contains any forbidden tech term (case-insensitive)
- Require minimum 2 words (first + last name)
- Keep existing validations (length, alphabetic ratio, sentence detection)

## Validation Flow

```
spaCy extracts "Seaborn" as PERSON
    ↓
is_valid_name("Seaborn")
    ↓
Check: "seaborn" in FORBIDDEN_NAMES? → YES
    ↓
REJECTED ❌
    ↓
Continue to next PERSON entity
```

## Test Cases

| Input | Before | After |
|-------|--------|-------|
| "Seaborn" | ❌ Accepted as name | ✅ Rejected (forbidden) |
| "Adobe XD" | ❌ Accepted as name | ✅ Rejected (forbidden) |
| "Python" | ❌ Accepted as name | ✅ Rejected (forbidden) |
| "John" | ✅ Accepted | ❌ Rejected (only 1 word) |
| "John Doe" | ✅ Accepted | ✅ Accepted |
| "Rahul Sharma" | ✅ Accepted | ✅ Accepted |

## Benefits

1. **Prevents false positives**: Tech skills no longer extracted as names
2. **Enforces proper names**: Requires first + last name (2+ words)
3. **Comprehensive coverage**: 50+ forbidden tech terms
4. **Case-insensitive**: Catches "Python", "python", "PYTHON"
5. **Substring matching**: Catches "Adobe XD" (contains "adobe")

## Restart Required

To apply the fix:
```bash
docker-compose down
docker-compose up --build
```

---

**Status**: ✅ **FIXED** - Tech skills are now properly filtered out from name extraction.
