"""Main bot implementation"""
import os
import json
from datetime import datetime

class InterviewBot:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, 'questions_db.json')
        self.questions_db = None
        self.companies_cache = None
        self.categories_cache = None
        self.search_history = {}
        self.difficulty_levels = ["Basic", "Medium", "Advanced"]  # Added difficulty levels
        # Load questions directly from local file
        self.load_questions()
        
    def load_questions(self):
        """Load questions from the JSON database"""
        try:
            if not self.questions_db:  # Load only if not already loaded
                with open(self.db_path, 'r', encoding='utf-8') as file:
                    self.questions_db = json.load(file)
                # Cache commonly accessed data
                self.companies_cache = list(self.questions_db.get("companies", {}).keys())
                self.categories_cache = self.questions_db.get("categories", {})
        except Exception as e:
            print(f"Error loading questions: {str(e)}")
            # Initialize with empty data if file can't be loaded
            self.questions_db = {"companies": {}, "categories": {}}
            self.companies_cache = []
            self.categories_cache = {}

    def get_experience_range(self, years):
        """Determine the experience range category"""
        try:
            years = float(years)
            if years <= 2:
                return "0-2"
            elif years <= 5:
                return "2-5"
            else:
                return "5+"
        except:
            return "0-2"  # Default to entry level if invalid input

    def get_interview_questions(self, company, years_of_experience, category=None, difficulty=None):
        """Get relevant interview questions based on company and experience"""
        try:
            if not company or not isinstance(company, str):
                return {"status": "error", "message": "Please provide a valid company name."}
            
            company = company.strip()
            exp_range = self.get_experience_range(years_of_experience)
            
            # Use general questions if company not found
            if company not in (self.questions_db.get("companies") or {}):
                questions = self.questions_db.get("companies", {}).get("Popular Interview Questions", {}).get(exp_range, [])
            else:
                questions = self.questions_db.get("companies", {}).get(company, {}).get(exp_range, [])
            
            # Apply filters
            if category:
                questions = [q for q in questions if q.get("category") == category]
            
            if difficulty:
                questions = [q for q in questions if q.get("difficulty") == difficulty]
            
            return {
                "status": "success",
                "company": company,
                "experience_range": exp_range,
                "questions": questions
            }
        except Exception as e:
            return {"status": "error", "message": f"Error fetching questions: {str(e)}"}

    def get_categories(self):
        """Get all available categories"""
        return self.categories_cache or {}

    def get_available_companies(self):
        """Get list of all companies in the database"""
        return self.companies_cache or []

    def get_difficulty_levels(self):
        """Get list of available difficulty levels"""
        return self.difficulty_levels

    def format_response(self, response):
        """Format the response in a readable way"""
        if response.get("status") in ["error", "partial"]:
            return f"Error: {response.get('message', 'Unknown error occurred')}"

        output = f"\nInterview Questions for {response.get('company')} "
        output += f"({response.get('experience_range')} years experience)\n"
        output += "=" * 80 + "\n\n"

        for i, q in enumerate(response.get("questions", []), 1):
            output += f"Question #{i}:\n"
            output += f"Category: {q.get('category', 'General')}\n"
            output += f"Q: {q.get('question')}\n"
            if q.get('answer'):
                output += f"A: {q.get('answer')}\n"
            output += "-" * 40 + "\n\n"

        return output