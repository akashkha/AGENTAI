"""Main bot implementation"""
import os
import json
from datetime import datetime
from .settings import get_db_path
from .web_search import search_interview_questions

class InterviewBot:
    def __init__(self):
        try:
            # Print current working directory for debugging
            current_dir = os.getcwd()
            print(f"Current working directory: {current_dir}")
            print(f"Current file location: {os.path.abspath(__file__)}")
            
            # Initialize with default questions
            self.default_questions = {
                "0-2": [
                    {
                        "question": "What are the main components of Selenium WebDriver?",
                        "answer": "Main components:\n1. WebDriver\n2. WebElement\n3. Select class\n4. Alert interface\n5. Navigation interface",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    }
                ],
                "2-5": [
                    {
                        "question": "How do you implement data-driven testing in Selenium?",
                        "answer": "Data-driven implementation:\n1. External data sources\n2. TestNG DataProvider\n3. Excel/CSV integration\n4. Parameter handling\n5. Test data management",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    }
                ]
            }
            
            # Look for questions_db.json in the interview_bot package directory
            self.db_path = os.path.join(os.path.dirname(__file__), 'questions_db.json')
            if not os.path.exists(self.db_path):
                print(f"Database not found at: {self.db_path}")
                raise FileNotFoundError("Could not find questions_db.json")
            print(f"Found database at: {self.db_path}")
                
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
        print(f"Getting questions for {company}, exp: {years_of_experience}, category: {category}, difficulty: {difficulty}")
        try:
            # Always start with default questions
            exp_range = self.get_experience_range(years_of_experience)
            questions = self.default_questions.get(exp_range, [])
            
            # Add web search results
            web_results = search_interview_questions(company)
            questions.extend(web_results)
            
            # Ensure all questions have proper metadata
            for q in questions:
                if not q.get('category'):
                    q['category'] = 'Selenium'
                if not q.get('difficulty'):
                    q['difficulty'] = 'Basic'
                if not q.get('type'):
                    q['type'] = 'Technical'
                q['experience_range'] = exp_range
            
            # Apply filters if specified
            if category and category != 'All':
                filtered = [q for q in questions if q.get('category') == category]
                if filtered:
                    questions = filtered
            
            if difficulty and difficulty != 'All':
                filtered = [q for q in questions if q.get('difficulty') == difficulty]
                if filtered:
                    questions = filtered
            
            print(f"Returning {len(questions)} questions")
            return {
                "status": "success",
                "company": company,
                "experience_range": exp_range,
                "questions": questions
            }
            if not company or not isinstance(company, str):
                return {"status": "error", "message": "Please provide a valid company name."}
            
            company = company.strip()
            exp_range = self.get_experience_range(years_of_experience)
            questions = []
            
            # Check if exact company match exists
            if company in (self.questions_db.get("companies") or {}):
                questions = self.questions_db.get("companies", {}).get(company, {}).get(exp_range, [])
            else:
                # Search across all companies for relevant questions
                company_lower = company.lower()
                for comp, data in self.questions_db.get("companies", {}).items():
                    exp_questions = data.get(exp_range, [])
                    for q in exp_questions:
                        # Check question text and answer for relevance
                        if (company_lower in q.get('question', '').lower() or 
                            company_lower in q.get('answer', '').lower()):
                            q_copy = q.copy()
                            q_copy['original_company'] = comp
                            questions.append(q_copy)
            
            # Always get web results to ensure comprehensive coverage
            web_results = search_interview_questions(company)
            for q in web_results:
                q['experience_range'] = exp_range
                questions.append(q)
            
            # Ensure questions are unique and relevant
            seen = set()
            unique_questions = []
            for q in questions:
                q_text = q.get('question', '')
                if q_text not in seen:
                    seen.add(q_text)
                    unique_questions.append(q)
            questions = unique_questions
            
            # Ensure all questions have category and difficulty
            for q in questions:
                q['category'] = q.get('category', 'Selenium')
                q['difficulty'] = q.get('difficulty', 'Basic')
                q['experience_range'] = exp_range
            
            # Keep track of original questions
            all_questions = questions.copy()
            
            # Apply filters
            if category and category != "All":
                questions = [q for q in questions if q.get('category') == category]
            
            if difficulty and difficulty != "All":
                questions = [q for q in questions if q.get('difficulty') == difficulty]
            
            # If no questions match filters, return all questions with default values
            if not questions:
                print(f"No questions after filtering. Returning all questions with default values")
                questions = all_questions
            
            # If we have few or no results, search online
            if not questions or len(questions) < 3:
                web_results = search_interview_questions(company)            # If few or no results, search online
            if len(questions) < 3:
                web_results = search_interview_questions(company)
                for result in web_results:
                    result['experience_range'] = exp_range
                    questions.append(result)            # Apply filters
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
            if 'original_company' in q:
                output += f"[Found in {q['original_company']} interviews]\n"
            elif 'source' in q:
                output += f"[Found from online source]\n"
            output += f"Category: {q.get('category', 'General')}\n"
            output += f"Q: {q.get('question')}\n"
            if q.get('answer'):
                output += f"A: {q.get('answer')}\n"
            if q.get('followup'):
                output += f"Follow-up: {q.get('followup')}\n"
            if q.get('followup_answer'):
                output += f"Follow-up Answer: {q.get('followup_answer')}\n"
            output += "-" * 40 + "\n\n"

        return output