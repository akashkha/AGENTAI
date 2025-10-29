import os
import json

def get_db_path():
    """Get the path to the questions database"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions_db.json')
    
    if os.path.exists(path):
        print(f"Found database at: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                # Verify it's valid JSON
                json.load(f)
            return path
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in questions_db.json")
    
    raise FileNotFoundError("Could not find questions_db.json")
