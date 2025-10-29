import json
import os
from datetime import datetime
try:
    from .string_matcher import find_closest_match
except ImportError:
    from string_matcher import find_closest_match

class InterviewBot:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'questions_db.json')
        self.questions_db = None
        self.companies_cache = None
        self.categories_cache = None
        from question_aggregator import QuestionAggregator
        self.aggregator = QuestionAggregator()
        self.search_history = {}
        self.coding_questions = {
            "Automation": {
                "Easy": [
                    {
                        "question": "Write a function to handle dynamic waits in Selenium",
                        "category": "Automation",
                        "difficulty": "Easy",
                        "code_template": """def wait_for_element(driver, locator, timeout=10):
    # TODO: Implement dynamic wait logic
    pass""",
                        "solution": """from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        return None""",
                        "alternative_solutions": [
                            {
                                "description": "Using custom polling function",
                                "code": """def wait_for_element(driver, locator, timeout=10, poll_frequency=0.5):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            element = driver.find_element(*locator)
            if element.is_displayed():
                return element
        except:
            pass
        time.sleep(poll_frequency)
    return None"""
                            },
                            {
                                "description": "Using multiple conditions",
                                "code": """def wait_for_element(driver, locator, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(*locator) and 
                      d.find_element(*locator).is_displayed() and 
                      d.find_element(*locator).is_enabled()
        )
        return element
    except TimeoutException:
        return None"""
                            }
                        ],
                        "test_cases": ["Basic element wait", "Timeout scenario", "Multiple elements"],
                        "hints": ["Use WebDriverWait", "Consider expected_conditions", "Handle TimeoutException"]
                    }
                ]
            }
        }
        
    def search_internet(self, query, category=None):
        """Search internet for additional information based on query type"""
        try:
            # Check if we already have cached results
            cache_key = f"{category}_{query}" if category else query
            if cache_key in self.search_history:
                return self.search_history[cache_key]
            
            # Define search sources based on category
            sources = {
                'technical': [
                    ('stackoverflow.com', 'programming solutions'),
                    ('github.com', 'code examples'),
                    ('medium.com', 'programming tutorials')
                ],
                'behavioral': [
                    ('indeed.com', 'interview questions'),
                    ('glassdoor.com', 'interview experiences'),
                    ('linkedin.com', 'career advice')
                ],
                'system_design': [
                    ('highscalability.com', 'system design'),
                    ('github.com', 'architecture examples'),
                    ('medium.com', 'system design interview')
                ],
                'hr': [
                    ('indeed.com', 'HR interview questions'),
                    ('glassdoor.com', 'HR round'),
                    ('thebalancecareers.com', 'HR interview')
                ],
                'general': [
                    ('indeed.com', 'interview questions'),
                    ('glassdoor.com', 'interview'),
                    ('linkedin.com', 'career advice')
                ]
            }
            
            # Determine the type of question
            question_type = category if category in sources else 'general'
            if not category:
                # Try to infer category from query
                tech_keywords = ['code', 'program', 'algorithm', 'function', 'api', 'test', 'debug', 'implement']
                behavioral_keywords = ['challenge', 'conflict', 'team', 'leadership', 'mistake', 'achievement']
                system_keywords = ['design', 'architecture', 'scale', 'database', 'microservice', 'system']
                hr_keywords = ['salary', 'notice', 'joining', 'relocation', 'package', 'benefits']
                
                query_lower = query.lower()
                if any(keyword in query_lower for keyword in tech_keywords):
                    question_type = 'technical'
                elif any(keyword in query_lower for keyword in behavioral_keywords):
                    question_type = 'behavioral'
                elif any(keyword in query_lower for keyword in system_keywords):
                    question_type = 'system_design'
                elif any(keyword in query_lower for keyword in hr_keywords):
                    question_type = 'hr'
            
            # Build search URLs based on question type
            search_urls = []
            for site, context in sources[question_type]:
                search_urls.append(f"https://www.google.com/search?q={query}+{context}+site:{site}")
            
            # Add company-specific search if company name is in query
            company_name = None
            for company in self.get_companies():
                if company.lower() in query.lower():
                    company_name = company
                    company_search = f"https://www.google.com/search?q={query}+{company}+interview+experience"
                    search_urls.insert(0, company_search)  # Prioritize company-specific results
                    break
            
            results = fetch_webpage(urls=search_urls, query=query)
            if results:
                formatted_results = self._format_search_results(results, company_name)
                self.search_history[cache_key] = formatted_results
                return formatted_results
            return None
        except Exception as e:
            print(f"Error searching internet: {str(e)}")
            return None
            
    def _format_search_results(self, results, company_name=None):
        """Format search results with relevant sections and highlights"""
        formatted = ""
        
        if company_name:
            formatted += f"Information specific to {company_name}:\n"
            formatted += "-" * 40 + "\n"
        
        formatted += "Key Points:\n"
        formatted += results + "\n\n"
        
        formatted += "Note: This information is gathered from public sources and should be used as a general guide."
        return formatted

    def get_coding_categories(self):
        """Get list of all coding question categories"""
        return list(self.coding_questions.keys())
    
    def get_coding_difficulties(self, category):
        """Get list of difficulties for a category"""
        if category in self.coding_questions:
            return list(self.coding_questions[category].keys())
        return []
    
    def get_coding_question(self, category, difficulty):
        """Get a random coding question for given category and difficulty"""
        import random
        if category in self.coding_questions and difficulty in self.coding_questions[category]:
            questions = self.coding_questions[category][difficulty]
            if questions:
                return random.choice(questions)
        return None

    # ... [rest of the original InterviewBot class implementation] ...
