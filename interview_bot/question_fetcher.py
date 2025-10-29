import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import json
import os
from datetime import datetime

class InterviewQuestionsFetcher:
    def __init__(self):
        self.cache_file = 'interview_questions_cache.json'
        self.cache = self._load_cache()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _load_cache(self) -> dict:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def fetch_questions(self, company_name: str, category: str = None) -> List[Dict]:
        """Fetch interview questions for a specific company and category"""
        cache_key = f"{company_name}_{category}" if category else company_name
        
        # Check cache first
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            # Cache for 7 days
            if (datetime.now() - datetime.fromisoformat(cache_entry['timestamp'])).days < 7:
                return cache_entry['data']

        results = []
        
        # Define search queries
        search_queries = [
            f"{company_name} interview questions",
            f"{company_name} interview experience"
        ]
        
        if category:
            search_queries.extend([
                f"{company_name} {category} interview questions",
                f"{category} questions in {company_name} interviews"
            ])

        # Define sources to search
        sources = [
            "glassdoor.com",
            "leetcode.com",
            "geeksforgeeks.org",
            "interviewbit.com",
            "ambitionbox.com"
        ]

        for query in search_queries:
            for source in sources:
                try:
                    # Construct search URL
                    url = f"https://www.google.com/search?q=site:{source}+{query}"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'lxml')
                        
                        # Extract search results
                        search_results = soup.find_all('div', class_='g')
                        
                        for result in search_results:
                            # Extract title and snippet
                            title = result.find('h3')
                            snippet = result.find('div', class_='VwiC3b')
                            link = result.find('a')
                            
                            if title and snippet and link:
                                results.append({
                                    'question': title.text.strip(),
                                    'answer': snippet.text.strip(),
                                    'source': link['href'],
                                    'category': category
                                })

                except Exception as e:
                    continue

        # Process and clean results
        cleaned_results = []
        for result in results:
            # Clean and format the question
            question = re.sub(r'\s+', ' ', result['question'])
            answer = re.sub(r'\s+', ' ', result['answer'])
            
            if self._is_valid_question(question):
                cleaned_results.append({
                    'question': question,
                    'answer': answer,
                    'source': result['source'],
                    'category': result['category']
                })

        # Cache the results
        self.cache[cache_key] = {
            'timestamp': datetime.now().isoformat(),
            'data': cleaned_results
        }
        self._save_cache()

        return cleaned_results

    def _is_valid_question(self, text: str) -> bool:
        """Check if the text appears to be a valid interview question"""
        # Common patterns for interview questions
        question_patterns = [
            r'\?$',
            r'^what',
            r'^how',
            r'^explain',
            r'^describe',
            r'^implement',
            r'^write',
            r'^design',
            r'difference between'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in question_patterns)

    def get_question_categories(self) -> List[str]:
        """Return available question categories"""
        return [
            "Technical",
            "System Design",
            "Behavioral",
            "HR",
            "Coding",
            "Database",
            "Testing",
            "DevOps",
            "Architecture",
            "Project Management"
        ]

    def format_results(self, results: List[Dict], company_name: str) -> str:
        """Format the results into a readable string"""
        if not results:
            return f"No specific interview questions found for {company_name}. Try different search terms or categories."

        formatted = f"Interview Questions for {company_name}\n"
        formatted += "=" * 50 + "\n\n"

        # Group questions by category
        questions_by_category = {}
        for result in results:
            category = result.get('category', 'General')
            if category not in questions_by_category:
                questions_by_category[category] = []
            questions_by_category[category].append(result)

        for category, questions in questions_by_category.items():
            formatted += f"\n{category} Questions:\n"
            formatted += "-" * 30 + "\n\n"
            
            for idx, q in enumerate(questions, 1):
                formatted += f"Q{idx}. {q['question']}\n"
                if q.get('answer'):
                    formatted += f"Answer: {q['answer']}\n"
                formatted += f"Source: {q['source']}\n\n"

        formatted += "\nNote: Questions are collected from public sources. Always prepare thoroughly!"
        return formatted