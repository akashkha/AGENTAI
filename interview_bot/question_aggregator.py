import json
import os
from datetime import datetime

class QuestionAggregator:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'questions_db_fixed.json')
        self.questions_db = None
        self.company_info = {
            'FAANG': {
                'Google': {'domains': ['technology', 'cloud', 'ai'], 'focus': ['system design', 'algorithms', 'automation']},
                'Amazon': {'domains': ['ecommerce', 'cloud', 'technology'], 'focus': ['automation', 'devops', 'testing']},
                'Meta': {'domains': ['technology', 'social', 'ai'], 'focus': ['frontend', 'backend', 'automation']},
                'Apple': {'domains': ['technology', 'hardware'], 'focus': ['quality', 'user experience', 'automation']},
                'Netflix': {'domains': ['streaming', 'technology'], 'focus': ['performance', 'scalability', 'automation']}
            },
            'Financial': {
                'JPMorgan': {'domains': ['banking', 'fintech'], 'focus': ['security', 'performance']},
                'Goldman Sachs': {'domains': ['banking', 'trading'], 'focus': ['algorithms', 'performance']},
                'Morgan Stanley': {'domains': ['banking', 'investment'], 'focus': ['stability', 'security']},
                'Barclays': {'domains': ['banking', 'fintech'], 'focus': ['security', 'automation']},
                'Citi': {'domains': ['banking', 'financial'], 'focus': ['integration', 'security']}
            },
            'Technology': {
                'Microsoft': {'domains': ['technology', 'cloud'], 'focus': ['quality', 'automation']},
                'IBM': {'domains': ['technology', 'consulting'], 'focus': ['enterprise', 'automation']},
                'Oracle': {'domains': ['database', 'cloud'], 'focus': ['performance', 'security']},
                'SAP': {'domains': ['enterprise', 'erp'], 'focus': ['integration', 'automation']},
                'Salesforce': {'domains': ['crm', 'cloud'], 'focus': ['customization', 'automation']}
            },
            'Consulting': {
                'Accenture': {'domains': ['consulting', 'technology'], 'focus': ['integration', 'automation']},
                'Deloitte': {'domains': ['consulting', 'audit'], 'focus': ['process', 'quality']},
                'Capgemini': {'domains': ['consulting', 'technology'], 'focus': ['methodology', 'automation']},
                'Cognizant': {'domains': ['technology', 'consulting'], 'focus': ['delivery', 'quality']},
                'TCS': {'domains': ['technology', 'services'], 'focus': ['process', 'automation']}
            }
        }
        self.load_questions()

    def load_questions(self):
        """Load existing questions database"""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as file:
                data = file.read()
                try:
                    self.questions_db = json.loads(data)
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON at position {e.pos}: {e.msg}")
                    # Initialize empty database if loading fails
                    self.questions_db = {
                        "sources": {},
                        "companies": {},
                        "categories": {},
                        "difficulty_levels": {},
                        "experience_ranges": {}
                    }
        else:
            self.questions_db = {
                "sources": {},
                "companies": {},
                "categories": {},
                "difficulty_levels": {},
                "experience_ranges": {}
            }

    def save_questions(self):
        """Save questions database to file"""
        with open(self.db_path, 'w') as file:
            json.dump(self.questions_db, file, indent=2)

    def generate_company_questions(self, company_name):
        """Generate relevant questions based on company profile"""
        company_info = None
        for category, companies in self.company_info.items():
            if company_name in companies:
                company_info = companies[company_name]
                break

        if not company_info:
            return []

        domains = company_info['domains']
        focus_areas = company_info['focus']
        
        questions = {
            "0-2": self._generate_junior_questions(domains, focus_areas),
            "2-5": self._generate_senior_questions(domains, focus_areas)
        }
        
        return questions

    def _generate_junior_questions(self, domains, focus_areas):
        """Generate questions for 0-2 years experience"""
        questions = []
        
        # Core automation questions
        questions.extend([
            {
                "question": f"How would you implement automated testing for a {domain} application?",
                "category": "Framework Design",
                "difficulty": "Medium",
                "date_asked": datetime.now().strftime("%Y-%m"),
                "type": "Technical",
                "answer": f"Implementation steps:\n1. Analyze {domain} requirements\n2. Choose appropriate tools\n3. Design framework architecture\n4. Implement core components\n5. Add reporting and logging\n6. Set up CI/CD integration",
                "followup": "How would you handle test data management?",
                "followup_answer": "Test data approach:\n1. Data generation strategies\n2. Environment management\n3. Data cleanup procedures\n4. Version control for test data"
            } for domain in domains
        ])
        
        # Tool-specific questions
        for focus in focus_areas:
            questions.append({
                "question": f"Explain your experience with {focus} testing",
                "category": focus.title(),
                "difficulty": "Medium",
                "date_asked": datetime.now().strftime("%Y-%m"),
                "type": "Technical",
                "answer": f"{focus.title()} testing approach:\n1. Test strategy\n2. Tool selection\n3. Implementation methods\n4. Best practices\n5. Common challenges",
                "followup": f"What challenges did you face in {focus} testing?",
                "followup_answer": "Common challenges:\n1. Environment setup\n2. Tool limitations\n3. Integration issues\n4. Performance impact"
            })
        
        return questions

    def _generate_senior_questions(self, domains, focus_areas):
        """Generate questions for 2-5 years experience"""
        questions = []
        
        # Architecture and design questions
        for domain in domains:
            questions.append({
                "question": f"Design a test automation framework for a {domain} platform",
                "category": "System Design",
                "difficulty": "Advanced",
                "date_asked": datetime.now().strftime("%Y-%m"),
                "type": "Design",
                "answer": f"Framework design for {domain}:\n1. Architecture overview\n2. Component design\n3. Integration patterns\n4. Scalability approach\n5. Security considerations",
                "followup": "How would you ensure framework maintainability?",
                "followup_answer": "Maintainability strategy:\n1. Code standards\n2. Documentation\n3. Review process\n4. Training plan"
            })
        
        # Advanced technical questions
        for focus in focus_areas:
            questions.append({
                "question": f"How would you implement {focus} automation at scale?",
                "category": focus.title(),
                "difficulty": "Advanced",
                "date_asked": datetime.now().strftime("%Y-%m"),
                "type": "Technical",
                "answer": f"Scaling {focus} automation:\n1. Infrastructure setup\n2. Resource management\n3. Performance optimization\n4. Monitoring and alerts\n5. Disaster recovery",
                "followup": f"What metrics would you track for {focus} automation?",
                "followup_answer": "Key metrics:\n1. Execution time\n2. Success rate\n3. Coverage metrics\n4. Resource utilization"
            })
        
        return questions

    def add_company_questions(self, company_name):
        """Add or update questions for a specific company"""
        questions = self.generate_company_questions(company_name)
        if questions:
            self.questions_db["companies"][company_name] = questions
            self.save_questions()
            return True
        return False

    def bulk_update_companies(self):
        """Update questions for all known companies"""
        for category, companies in self.company_info.items():
            for company_name in companies:
                self.add_company_questions(company_name)
        self.save_questions()

def update_question_database():
    """Update the entire question database with fresh questions"""
    aggregator = QuestionAggregator()
    aggregator.bulk_update_companies()