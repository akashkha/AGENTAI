import os
import json

def get_db_path():
    """Get the path to the questions database"""
    paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions_db.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'interview_bot', 'questions_db.json'),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'questions_db.json')
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"Found database at: {path}")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    # Verify it's valid JSON
                    json.load(f)
                return path
            except json.JSONDecodeError:
                continue
    
    raise FileNotFoundError("Could not find valid questions_db.json in any location")