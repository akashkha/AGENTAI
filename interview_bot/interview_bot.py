import json
import os
from datetime import datetime
import os
import sys
import json
from datetime import datetime

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from string_matcher import find_closest_match
from question_aggregator import QuestionAggregator
from search_engine import SearchEngine

class InterviewBot:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, 'questions_db.json')
        self.questions_db = None
        self.companies_cache = None
        self.categories_cache = None
        self.search_engine = SearchEngine()
        self.search_history = {}
        # Load questions directly from local file
        self.load_questions()
        
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
                    },
                    {
                        "question": "Create a function to handle file uploads in automation",
                        "category": "Automation",
                        "difficulty": "Easy",
                        "code_template": """def upload_file(driver, file_input_locator, file_path):
    # TODO: Implement file upload logic
    pass""",
                        "solution": """def upload_file(driver, file_input_locator, file_path):
    try:
        file_input = driver.find_element(*file_input_locator)
        file_input.send_keys(file_path)
        return True
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False""",
                        "test_cases": ["Valid file upload", "Invalid file path", "Non-existent element"],
                        "hints": ["Use send_keys()", "Verify file path exists", "Handle exceptions"]
                    }
                ],
                "Medium": [
                    {
                        "question": "Implement a custom retry mechanism for flaky tests",
                        "category": "Automation",
                        "difficulty": "Medium",
                        "code_template": """class RetryAnalyzer:
    def __init__(self, max_retry=3):
        # TODO: Implement retry logic
        pass""",
                        "solution": """class RetryAnalyzer:
    def __init__(self, max_retry=3):
        self.max_retry = max_retry
        self.count = 0
    
    def retry(self, result):
        if self.count < self.max_retry:
            self.count += 1
            print(f"Retrying test, attempt {self.count}")
            return True
        return False""",
                        "test_cases": ["Successful retry", "Max retries exceeded", "Reset counter"],
                        "hints": ["Track retry count", "Set max retries", "Consider test result"]
                    }
                ],
                "Hard": [
                    {
                        "question": "Design a test data generator for API testing",
                        "category": "Automation",
                        "difficulty": "Hard",
                        "code_template": """class TestDataGenerator:
    def __init__(self):
        # TODO: Implement data generation logic
        pass""",
                        "solution": """import random
import string
from datetime import datetime, timedelta

class TestDataGenerator:
    def __init__(self):
        self.data_types = {
            'string': self._generate_string,
            'email': self._generate_email,
            'date': self._generate_date,
            'number': self._generate_number
        }
    
    def _generate_string(self, length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def _generate_email(self):
        name = self._generate_string(8)
        return f"{name}@example.com"
    
    def _generate_date(self):
        days = random.randint(-365, 365)
        return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    
    def _generate_number(self, min_val=0, max_val=1000):
        return random.randint(min_val, max_val)
    
    def generate_data(self, schema):
        result = {}
        for field, field_type in schema.items():
            result[field] = self.data_types[field_type]()
        return result""",
                        "test_cases": ["Generate string data", "Generate date data", "Complex schema"],
                        "hints": ["Use data type handlers", "Consider edge cases", "Validate output"]
                    }
                ]
            },
            "DSA": {
                "Easy": [
                    {
                        "question": "Implement a stack for storing test results",
                        "category": "DSA",
                        "difficulty": "Easy",
                        "code_template": """class TestResultStack:
    def __init__(self):
        # TODO: Initialize stack
        pass""",
                        "solution": """class TestResultStack:
    def __init__(self):
        self.stack = []
    
    def push(self, result):
        self.stack.append(result)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)""",
                        "test_cases": ["Push elements", "Pop elements", "Empty stack"],
                        "hints": ["Use list operations", "Check empty condition", "LIFO principle"]
                    }
                ]
            },
            "API Testing": {
                "Easy": [
                    {
                        "question": "Write a function to validate API response schema",
                        "category": "API Testing",
                        "difficulty": "Easy",
                        "code_template": """def validate_response_schema(response, expected_schema):
    # TODO: Implement schema validation
    pass""",
                        "solution": """def validate_response_schema(response, expected_schema):
    try:
        response_json = response.json()
        for field, field_type in expected_schema.items():
            if field not in response_json:
                return False
            if not isinstance(response_json[field], field_type):
                return False
        return True
    except Exception:
        return False""",
                        "test_cases": ["Valid schema", "Missing fields", "Invalid types"],
                        "hints": ["Check field presence", "Verify data types", "Handle JSON parsing"]
                    }
                ]
            }
        }
        self.domains_cache = {
            'ecommerce': ['Amazon India', 'Flipkart', 'Walmart'],
            'fintech': ['PhonePe', 'Paytm', 'Mastercard', 'Visa'],
            'banking': ['Barclays', 'Citi Bank', 'HSBC', 'Deutsche Bank', 'Goldman Sachs', 'JPMorgan'],
            'food_delivery': ['Swiggy', 'Zomato', 'UberEats'],
            'technology': ['Microsoft India', 'TCS', 'Infosys', 'Wipro', 'Amdocs', 'Accenture', 'Nagarro', 'Cognizant', 'HCL', 'IBM'],
            'telecom': ['Amdocs', 'Ericsson', 'Nokia', 'Vodafone', 'AT&T'],
            'automotive': ['BMW', 'Mercedes', 'Bosch', 'Continental'],
            'healthcare': ['Philips', 'Siemens Healthineers', 'GE Healthcare'],
            'general': ['Popular Interview Questions', 'Common Coding Challenges']
        }
        self.company_aliases = {
            # Technology Companies
            'amdocs': 'technology',
            'tcs': 'technology',
            'infosys': 'technology',
            'wipro': 'technology',
            'microsoft': 'technology',
            'accenture': 'technology',
            'nagarro': 'technology',
            'cognizant': 'technology',
            'capgemini': 'technology',
            'hcl': 'technology',
            'ibm': 'technology',
            'oracle': 'technology',
            'sap': 'technology',
            'dell': 'technology',
            'hp': 'technology',
            
            # Ecommerce
            'amazon': 'ecommerce',
            'flipkart': 'ecommerce',
            'walmart': 'ecommerce',
            'target': 'ecommerce',
            
            # Fintech & Banking
            'mastercard': 'fintech',
            'visa': 'fintech',
            'phonepe': 'fintech',
            'paytm': 'fintech',
            'razorpay': 'fintech',
            'barclays': 'banking',
            'citi': 'banking',
            'hsbc': 'banking',
            'deutsche': 'banking',
            'goldman': 'banking',
            'jpmorgan': 'banking',
            'morgan': 'banking',
            
            # Food Delivery
            'swiggy': 'food_delivery',
            'zomato': 'food_delivery',
            'uber': 'food_delivery',
            
            # Automotive
            'bmw': 'automotive',
            'mercedes': 'automotive',
            'bosch': 'automotive',
            'continental': 'automotive',
            
            # Healthcare
            'philips': 'healthcare',
            'siemens': 'healthcare',
            'ge': 'healthcare'
        }
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

    def get_company_domain(self, company_name):
        """Determine the domain of a company based on its name or existing mappings"""
        company_key = company_name.lower().split()[0]  # Get first word of company name
        
        # Check company aliases first
        if company_key in self.company_aliases:
            return self.company_aliases[company_key]
        
        # Check if company exists in our domain mappings
        for domain, companies in self.domains_cache.items():
            if any(c.lower() in company_name.lower() for c in companies):
                return domain
        
        # Use keyword matching for unknown companies
        keywords = {
            'ecommerce': ['shop', 'retail', 'mart', 'buy', 'store', 'commerce', 'market', 'shopping', 'online'],
            'fintech': ['pay', 'finance', 'money', 'wallet', 'fin', 'cash', 'credit', 'card', 'payment', 'transaction'],
            'banking': ['bank', 'banking', 'investment', 'trading', 'financial', 'capital', 'asset', 'wealth', 'securities'],
            'food_delivery': ['food', 'delivery', 'restaurant', 'kitchen', 'meal', 'dining', 'cuisine', 'order'],
            'technology': ['tech', 'soft', 'it', 'system', 'digital', 'computer', 'software', 'labs', 'consulting', 'solutions', 'services'],
            'telecom': ['telecom', 'communication', 'network', 'mobile', 'wireless', 'broadband', 'telephony', 'cellular'],
            'automotive': ['auto', 'car', 'vehicle', 'motor', 'automotive', 'mobility', 'transport'],
            'healthcare': ['health', 'medical', 'hospital', 'care', 'pharma', 'diagnostic', 'clinical', 'biotech']
        }
        
        for domain, words in keywords.items():
            if any(word.lower() in company_name.lower() for word in words):
                return domain
        return 'general'

    def get_interview_questions(self, company, years_of_experience, category=None, difficulty=None):
        """Get relevant interview questions based on company and experience with optional filters"""
        try:
            # Input validation
            if not company or not isinstance(company, str):
                return {
                    "status": "error",
                    "message": "Please provide a valid company name."
                }
            
            company = company.strip()
            exp_range = self.get_experience_range(years_of_experience)
            
            # Try to generate questions if company not in database
            if company not in self.questions_db["companies"]:
                self.aggregator.add_company_questions(company)
            
            # Handle exact matches first (case-insensitive)
            exact_match = next((c for c in self.questions_db["companies"].keys() 
                              if c.lower() == company.lower()), None)
            if exact_match:
                company = exact_match
            else:
                # Try fuzzy matching
                matched_company, similarity = find_closest_match(company, self.questions_db["companies"].keys())
            
            # Determine company domain
            company_domain = self.get_company_domain(company)
            
            if not exact_match and (not matched_company or similarity < 0.6):  # If no close match found
                # Get domain-specific and general questions
                questions = []
                
                # Add questions from similar companies in the same domain
                for comp in self.domains_cache.get(company_domain, []):
                    if comp in self.questions_db["companies"]:
                        questions.extend(self.questions_db["companies"][comp].get(exp_range, []))
                
                # Add general questions
                questions.extend(self.questions_db["companies"]["Popular Interview Questions"].get(exp_range, []))
                
                # Add coding challenges for tech companies
                if company_domain == 'technology':
                    questions.extend(self.questions_db["companies"]["Common Coding Challenges"].get(exp_range, []))
                
                # Search internet for additional company-specific questions
                search_query = f"{company} interview questions {exp_range} years experience"
                if category:
                    search_query += f" {category}"
                if difficulty:
                    search_query += f" {difficulty}"
                
                online_results = self.search_internet(search_query, category)
                if online_results:
                    questions.append({
                        "question": "Additional Questions from Online Sources",
                        "category": category or "General",
                        "difficulty": difficulty or "Mixed",
                        "answer": online_results,
                        "source": "Internet Search",
                        "date_asked": "Recent",
                        "type": "Research-based"
                    })
                
                return {
                    "status": "success",
                    "company": f"{company} (using {company_domain} domain questions)",
                    "experience_range": exp_range,
                    "questions": questions,
                    "filters_applied": {
                        "category": category,
                        "difficulty": difficulty
                    }
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
=======

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
>>>>>>> 4f8dd752c6b6d73acc9ce3a04eb8b1f91cbcdfd8
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

    def get_categories(self):
        """Get all available categories"""
        if self.questions_db is None:
            self.load_questions()
        return self.categories_cache or {}

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

    def format_response(self, response):
        """Format the response in a readable way"""
        if response["status"] in ["error", "partial"]:
            error_msg = response["message"]
            help_msg = "\nYou can:\n- Ask for company specific questions\n- View question categories\n- List available companies\n- Type 'help' for more details"
            return f"{error_msg}\n{help_msg}"

        output = f"\nInterview Questions for {response['company']} ({response['experience_range']} years experience)\n"
        output += "=" * 80 + "\n\n"

        for i, q in enumerate(response["questions"], 1):
            output += f"Question #{i}:\n"
            output += f"==========\n"
            output += f"Topic: {q['question']}\n"
            output += f"Category: {q['category']}\n"
            output += f"Difficulty: {q['difficulty']}\n"
            output += f"Asked in: {q['date_asked']}\n"
            if "type" in q:
                output += f"Type: {q['type']}\n"
            if "answer" in q:
                output += f"\nAnswer:\n-------\n{q['answer']}\n"
            if "source" in q:
                output += f"Source: {q['source']}\n"
            if "company_reported" in q:
                output += f"Reported by candidates at: {', '.join(q['company_reported'])}\n"
            if "followup" in q:
                output += f"\nFollow-up Question:\n------------------\n{q['followup']}\n"
            if "followup_answer" in q:
                output += f"\nFollow-up Answer:\n---------------\n{q['followup_answer']}\n"
            output += "\n" + "=" * 80 + "\n\n"

        # Add category information
        categories = self.get_categories()
        if categories:
            output += "\nAvailable Categories:\n"
            for category, topics in categories.items():
                output += f"{category}: {', '.join(topics)}\n"

        return output
