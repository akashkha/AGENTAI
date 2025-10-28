import json
import os
from datetime import datetime
from interview_bot.string_matcher import find_closest_match

class InterviewBot:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'questions_db.json')
        self.questions_db = None
        self.companies_cache = None
        self.categories_cache = None
        self.load_questions()

    def load_questions(self):
        """Load questions from the JSON database"""
        if not self.questions_db:  # Load only if not already loaded
            with open(self.db_path, 'r') as file:
                self.questions_db = json.load(file)
            # Cache commonly accessed data
            self.companies_cache = list(self.questions_db["companies"].keys())
            self.categories_cache = self.questions_db.get("categories", {})

    def get_experience_range(self, years):
        """Determine the experience range category"""
        years = float(years)
        if years <= 2:
            return "0-2"
        elif years <= 5:
            return "2-5"
        else:
            return "2-5"  # Using 2-5 as default for higher experience

    def get_interview_questions(self, company, years_of_experience, category=None, difficulty=None):
        """Get relevant interview questions based on company and experience with optional filters"""
        try:
            exp_range = self.get_experience_range(years_of_experience)
            
            # Try to find the best matching company using fuzzy matching
            matched_company, similarity = find_closest_match(company, self.questions_db["companies"].keys())
            
            if not matched_company:
                return {
                    "status": "error",
                    "message": f"No matching company found for '{company}'. Available companies: {', '.join(self.get_available_companies())}"
                }
            
            # If it's not an exact match but close enough, inform the user
            if matched_company.lower() != company.lower():
                print(f"\nNote: Using '{matched_company}' as the closest match for your search '{company}'")
            
            company = matched_company

            questions = self.questions_db["companies"][company].get(exp_range, [])
            
            original_questions = questions[:]
            
            # Apply filters if provided
            if category:
                questions = self.filter_questions_by_category(questions, category)
            if difficulty:
                questions = self.filter_questions_by_difficulty(questions, difficulty)
            
            if not questions:
                alternative_suggestions = {
                    "same_category": [],
                    "same_difficulty": [],
                    "same_company": original_questions[:2]  # First 2 questions from same company
                }
                
                # Find questions with same category but different difficulty
                if category:
                    same_cat = self.filter_questions_by_category(original_questions, category)
                    alternative_suggestions["same_category"] = same_cat[:2]
                
                # Find questions with same difficulty but different category
                if difficulty:
                    same_diff = self.filter_questions_by_difficulty(original_questions, difficulty)
                    alternative_suggestions["same_difficulty"] = same_diff[:2]
                
                # Find similar questions from other companies
                other_company_questions = []
                for comp in self.questions_db["companies"]:
                    if comp != company and comp not in ["Popular Interview Questions", "Common Coding Challenges", "System Design Questions"]:
                        questions_list = self.questions_db["companies"][comp].get(exp_range, [])
                        if category:
                            questions_list = self.filter_questions_by_category(questions_list, category)
                        if difficulty:
                            questions_list = self.filter_questions_by_difficulty(questions_list, difficulty)
                        other_company_questions.extend(questions_list)
                
                filters = []
                if category:
                    filters.append(f"category '{category}'")
                if difficulty:
                    filters.append(f"difficulty '{difficulty}'")
                filter_msg = f" with {' and '.join(filters)}" if filters else ""
                
                message = f"No exact matches found for {company} with {exp_range} years experience range{filter_msg}.\n\n"
                
                # Add alternative suggestions
                if alternative_suggestions["same_company"]:
                    message += f"\nOther questions from {company} ({exp_range} years):\n"
                    for q in alternative_suggestions["same_company"]:
                        message += f"- {q['question']} (Category: {q['category']}, Difficulty: {q['difficulty']})\n"
                
                if alternative_suggestions["same_category"]:
                    message += f"\nQuestions with category '{category}' but different difficulty:\n"
                    for q in alternative_suggestions["same_category"]:
                        message += f"- {q['question']} (Difficulty: {q['difficulty']})\n"
                
                if alternative_suggestions["same_difficulty"]:
                    message += f"\nQuestions with difficulty '{difficulty}' but different category:\n"
                    for q in alternative_suggestions["same_difficulty"]:
                        message += f"- {q['question']} (Category: {q['category']})\n"
                
                if other_company_questions:
                    message += f"\nSimilar questions from other companies:\n"
                    for q in other_company_questions[:2]:  # Show up to 2 questions
                        message += f"- {q['question']}\n"
                
                message += "\nTip: Try adjusting the filters or selecting a different experience range for more results."
                
                return {
                    "status": "partial",
                    "message": message
                }

            return {
                "status": "success",
                "company": company,
                "experience_range": exp_range,
                "questions": questions,
                "filters_applied": {
                    "category": category,
                    "difficulty": difficulty
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error occurred: {str(e)}"
            }

    def get_categories(self):
        """Get all available categories"""
        return self.categories_cache

    def get_difficulty_levels(self):
        """Get all difficulty levels with descriptions"""
        return self.questions_db.get("difficulty_levels", {})

    def get_sources(self):
        """Get all question sources with descriptions"""
        return self.questions_db.get("sources", {})

    def get_available_companies(self):
        """Get list of all companies in the database"""
        return self.companies_cache

    def filter_questions_by_category(self, questions, category):
        """Filter questions by category"""
        return [q for q in questions if q["category"] == category]

    def filter_questions_by_difficulty(self, questions, difficulty):
        """Filter questions by difficulty level"""
        return [q for q in questions if q["difficulty"] == difficulty]

    def format_response(self, response):
        """Format the response in a readable way"""
        if response["status"] in ["error", "partial"]:
            return response["message"]

        output = f"\nInterview Questions for {response['company']} ({response['experience_range']} years experience):\n"
        output += "=" * 100 + "\n"

        for i, q in enumerate(response["questions"], 1):
            output += f"{i}. Question: {q['question']}\n"
            output += f"   Category: {q['category']}\n"
            output += f"   Difficulty: {q['difficulty']}\n"
            output += f"   Asked in: {q['date_asked']}\n"
            if "type" in q:
                output += f"   Type: {q['type']}\n"
            if "source" in q:
                output += f"   Source: {q['source']}\n"
            if "company_reported" in q:
                output += f"   Reported by candidates at: {', '.join(q['company_reported'])}\n"
            if "followup" in q:
                output += f"   Follow-up Question: {q['followup']}\n"
            output += "-" * 100 + "\n"

        # Add category information
        categories = self.get_categories()
        if categories:
            output += "\nAvailable Categories:\n"
            for category, topics in categories.items():
                output += f"{category}: {', '.join(topics)}\n"

        return output