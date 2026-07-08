import json
import os
import random
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


class InterviewBot:
    def __init__(self):
        self.db_path = os.path.join(current_dir, 'questions_db.json')
        self.questions_db = None
        self.companies_cache = None
        self.categories_cache = None
        self.search_history = {}
        self.coding_questions = self._build_coding_questions()
        self.load_questions()

    def _build_coding_questions(self):
        return {
            "Automation": {
                "Easy": [
                    {
                        "question": "Write a function to handle dynamic waits in Selenium",
                        "category": "Automation",
                        "difficulty": "Easy",
                        "code_template": "def wait_for_element(driver, locator, timeout=10):\n    # TODO: Implement dynamic wait logic\n    pass",
                        "solution": "from selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\n\ndef wait_for_element(driver, locator, timeout=10):\n    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))",
                        "test_cases": ["Basic element wait", "Timeout scenario"],
                        "hints": ["Use WebDriverWait", "Consider expected_conditions"],
                    }
                ],
                "Medium": [],
                "Hard": [],
            }
        }

    def load_questions(self):
        with open(self.db_path, 'r', encoding='utf-8') as f:
            self.questions_db = json.load(f)
        self.companies_cache = list(self.questions_db.get('companies', {}).keys())
        self.categories_cache = {}
        for company, data in self.questions_db.get('companies', {}).items():
            for experience_key, questions in data.items():
                for question in questions:
                    category = question.get('category')
                    if category:
                        self.categories_cache.setdefault(category, set()).add(question['question'])
        self.categories_cache = {k: sorted(v) for k, v in self.categories_cache.items()}

    def get_companies(self):
        return self.companies_cache or []

    def get_categories(self):
        return self.categories_cache or {}

    def get_difficulty_levels(self):
        return self.questions_db.get('difficulty_levels', {})

    def get_sources(self):
        return self.questions_db.get('sources', {})

    def get_available_companies(self):
        return self.companies_cache or []

    def filter_questions_by_category(self, questions, category):
        return [q for q in questions if q.get('category') == category]

    def filter_questions_by_difficulty(self, questions, difficulty):
        return [q for q in questions if q.get('difficulty') == difficulty]

    def get_coding_categories(self):
        return list(self.coding_questions.keys())

    def get_coding_difficulties(self, category):
        return list(self.coding_questions.get(category, {}).keys())

    def get_coding_question(self, category, difficulty):
        questions = self.coding_questions.get(category, {}).get(difficulty, [])
        return random.choice(questions) if questions else None

    def get_interview_questions(self, company, experience_range='2', filters=None):
        company_data = self.questions_db.get('companies', {}).get(company, {})
        experience_key = None
        for key in sorted(company_data.keys(), key=lambda x: int(x.split('-')[0])):
            start, end = [int(part) for part in key.split('-')]
            if int(experience_range) <= end:
                experience_key = key
                break
        if not experience_key:
            experience_key = '2-5'
        questions = company_data.get(experience_key, [])
        if filters:
            if filters.get('category'):
                questions = [q for q in questions if q.get('category') == filters['category']]
            if filters.get('difficulty'):
                questions = [q for q in questions if q.get('difficulty') == filters['difficulty']]
        return {
            'status': 'ok',
            'company': company,
            'experience_range': experience_range,
            'questions': questions,
        }

    def format_response(self, response):
        if response['status'] in ['error', 'partial']:
            error_msg = response['message']
            help_msg = '\nYou can:\n- Ask for company specific questions\n- View question categories\n- List available companies\n- Type \'help\' for more details'
            return f"{error_msg}\n{help_msg}"

        output = f"\nInterview Questions for {response['company']} ({response['experience_range']} years experience)\n"
        output += '=' * 80 + "\n\n"
        for i, q in enumerate(response['questions'], 1):
            output += f"Question #{i}:\n"
            output += f"==========\n"
            output += f"Topic: {q['question']}\n"
            output += f"Category: {q['category']}\n"
            output += f"Difficulty: {q['difficulty']}\n"
            output += f"Asked in: {q['date_asked']}\n"
            if 'type' in q:
                output += f"Type: {q['type']}\n"
            if 'answer' in q:
                output += f"\nAnswer:\n-------\n{q['answer']}\n"
            if 'followup' in q:
                output += f"\nFollow-up Question:\n------------------\n{q['followup']}\n"
            if 'followup_answer' in q:
                output += f"\nFollow-up Answer:\n---------------\n{q['followup_answer']}\n"
            output += "\n" + '=' * 80 + "\n\n"
        return output

    def search_internet(self, query, category=None):
        return None

    def _format_search_results(self, results, company_name=None):
        return results
