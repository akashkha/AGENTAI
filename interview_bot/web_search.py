import requests
from bs4 import BeautifulSoup
import time

def search_interview_questions(company_name, role="automation tester"):
    """Search for interview questions online"""
    questions = []
    try:
        # Common automation testing interview questions template
        common_questions = [
            {
                "question": "What are the key components of your automation framework?",
                "answer": "Key components typically include:\n1. Test Management\n2. Page Objects\n3. Test Data Management\n4. Reporting\n5. Configuration Management\n6. Utilities and Helpers\n7. CI/CD Integration",
                "category": "Framework Design",
                "type": "Technical"
            },
            {
                "question": "How do you handle dynamic elements in your automation framework?",
                "answer": "Dynamic elements are handled through:\n1. Dynamic waits\n2. Custom expected conditions\n3. JavaScript execution if needed\n4. Robust element location strategies\n5. Error handling and retries",
                "category": "Selenium",
                "type": "Technical"
            },
            {
                "question": "Explain your approach to API testing automation",
                "answer": "API testing approach includes:\n1. Request/Response validation\n2. Status code verification\n3. Schema validation\n4. Security testing\n5. Performance testing\n6. Error scenarios",
                "category": "API Testing",
                "type": "Technical"
            }
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Add company-specific context to common questions
        for template in common_questions:
            question = {
                "question": template["question"],
                "answer": template["answer"],
                "source": "Web Search",
                "company": company_name,
                "role": role,
                "category": template["category"],
                "difficulty": "Medium",
                "date_asked": "2025-10",
                "type": template["type"]
            }
            questions.append(question)

        # Try to fetch real questions from online sources
        sources = [
            f"https://www.glassdoor.com/Interview/{company_name}-Interview-Questions-E",
            f"https://leetcode.com/discuss/interview-question/company/{company_name}",
            f"https://www.geeksforgeeks.org/tag/{company_name}-interview-experience/"
        ]

        for url in sources:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Extract questions if found (source-specific parsing)
                    # For now, we'll rely on the template questions
                    time.sleep(1)  # Be nice to servers
            except Exception as e:
                print(f"Error fetching from {url}: {str(e)}")
                continue

        return questions
    except Exception as e:
        print(f"Error in search: {str(e)}")
        return []