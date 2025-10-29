import requests
from bs4 import BeautifulSoup
import time

def search_interview_questions(company_name, role="automation tester"):
    """Search for interview questions online"""
    questions = []
    try:
        # Create search query
        query = f"{company_name} {role} interview questions site:glassdoor.com OR site:leetcode.com OR site:geeksforgeeks.org"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Fetch results from different sources
        sources = [
            f"https://www.glassdoor.com/Interview/search.htm?keyword={company_name}%20{role}",
            f"https://leetcode.com/discuss/search?q={company_name}%20{role}%20interview",
            f"https://www.geeksforgeeks.org/search?q={company_name}+{role}+interview+questions"
        ]

        for url in sources:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.ok:
                    # Basic structure for found questions
                    question = {
                        "source": url,
                        "company": company_name,
                        "role": role,
                        "category": "External",
                        "difficulty": "Medium",
                        "date_asked": "2025-10",
                        "type": "Technical",
                    }
                    questions.append(question)
            except Exception as e:
                print(f"Error fetching from {url}: {str(e)}")
            time.sleep(1)  # Be nice to servers

        return questions
    except Exception as e:
        print(f"Error in search: {str(e)}")
        return []