
import sys
import os

# Add the project directory to sys.path
sys.path.append('/Users/sahulkumar/Documents/SAHUL/HACKTHON/HACKATHON/backend')

from app.resume_parser import ResumeParser

def reproduce():
    parser = ResumeParser()
    
    # User's actual case from screenshot
    text = """
SAHUL KUMAR
sahulshaw92@gmail.com 
Ghaziabad, India
    """
    email = "sahulshaw92@gmail.com"
    
    print(f"Testing with text:\n{text}")
    print(f"Email: {email}")
    
    result = parser.extract_name(text, email)
    print(f"\nResult: '{result}'")
    
    if result == "Sahul Umar":
        print("\n❌ REPRODUCED: 'Sahul Kumar' became 'Sahul Umar'!")
    elif result == "Sahul Kumar":
        print("\n✅ PASS: 'Sahul Kumar' was correctly extracted.")
    else:
        print(f"\n❓ UNEXPECTED RESULT: '{result}'")

if __name__ == "__main__":
    reproduce()
