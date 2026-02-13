
import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.resume_parser import ResumeParser

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_name_extraction():
    parser = ResumeParser()
    
    test_cases = [
        {
            "name": "Sahul Kumar (Correct)",
            "text": "Sahul Kumar\nSoftware Engineer\nsahulshawlike69@gmail.com",
            "email": "sahulshawlike69@gmail.com",
            "expected": "Sahul Kumar"
        },
        {
            "name": "Ahul Umar (OCR Error Case)",
            "text": "Ahul Umar\nSoftware Engineer\nsahulshawlike69@gmail.com",
            "email": "sahulshawlike69@gmail.com",
            "expected": "Sahul Kumar"
        },
        {
            "name": "Sahulshawkumar (Merged Case)",
            "text": "Sahul Kumar\nsahulshawlike69@gmail.com",
            "email": "sahulshawlike69@gmail.com",
            "expected": "Sahul Kumar"
        }
    ]
    
    print("\n--- Testing Name Extraction ---")
    for tc in test_cases:
        print(f"\nTest Case: {tc['name']}")
        result = parser.extract_name(tc['text'], tc['email'])
        print(f"Result: '{result}'")
        if result == tc['expected']:
            print("Status: ✅ PASS")
        else:
            print(f"Status: ❌ FAIL (Expected '{tc['expected']}')")

if __name__ == "__main__":
    test_name_extraction()
