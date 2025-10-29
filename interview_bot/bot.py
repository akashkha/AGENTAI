"""Main bot implementation"""
import os
import json
from datetime import datetime
from .settings import get_db_path

class InterviewBot:
    def __init__(self):
        try:
            # Print current working directory for debugging
            current_dir = os.getcwd()
            print(f"Current working directory: {current_dir}")
            print(f"Current file location: {os.path.abspath(__file__)}")
            
            # In deployed environment, look in current directory first
            possible_paths = [
                os.path.join(current_dir, 'questions_db.json'),  # Try current directory first
                os.path.join(current_dir, 'interview_bot', 'questions_db.json'),
                os.path.abspath(os.path.join(os.path.dirname(__file__), 'questions_db.json')),
                os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'questions_db.json'))
            ]
            
            # Try each path and use the first one that exists
            for path in possible_paths:
                print(f"Trying path: {path}")
                if os.path.exists(path):
                    print(f"Found database at: {path}")
                    self.db_path = path
                    break
            else:
                print("No database file found!")
                raise FileNotFoundError("Could not find questions_db.json")
                
            self.questions_db = None
            self.companies_cache = None
            self.categories_cache = None
            self.search_history = {}
            self.difficulty_levels = ["Basic", "Medium", "Advanced"]
            
            # Load questions
            self.load_questions()
            
            # Verify data is loaded
            if not self.companies_cache:
                print("Warning: No companies loaded!")
            else:
                print(f"Successfully loaded {len(self.companies_cache)} companies")
                
        except Exception as e:
            print(f"Error in InterviewBot initialization: {str(e)}")
            raise
        
    def load_questions(self):
        """Load questions from the JSON database"""
        if self.questions_db:  # Already loaded
            return
            
        try:
            print(f"Loading questions from: {self.db_path}")
            with open(self.db_path, 'r', encoding='utf-8') as file:
                self.questions_db = json.load(file)
            
            # Cache commonly accessed data
            if not self.questions_db:
                print("Warning: questions_db is empty!")
                raise ValueError("Database is empty or invalid")
            
            companies = self.questions_db.get("companies", {})
            if not companies:
                print("Warning: No companies found in database!")
                raise ValueError("No companies found in database")
                
            self.companies_cache = list(companies.keys())
            print(f"Loaded {len(self.companies_cache)} companies: {self.companies_cache}")
            
            categories = self.questions_db.get("categories", {})
            if not categories:
                print("Warning: No categories found in database!")
                raise ValueError("No categories found in database")
                
            self.categories_cache = categories
            print(f"Loaded {len(categories)} categories: {list(categories.keys())}")
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

    def search_questions(self, query):
        """Search for questions across all companies and categories"""
        query = query.lower()
        results = []
        
        # Search through all companies and their questions
        for company, exp_ranges in self.questions_db.get('companies', {}).items():
            for exp_range, questions in exp_ranges.items():
                for question in questions:
                    # Search in question text
                    if query in question.get('question', '').lower():
                        results.append({
                            'company': company,
                            'experience': exp_range,
                            'category': question.get('category', 'General'),
                            'difficulty': question.get('difficulty', 'Medium'),
                            'question': question.get('question'),
                            'answer': question.get('answer', '')
                        })
        
        return results

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