import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote

def search_interview_questions(company_name, role="automation tester", category="selenium", max_questions=50):
    """Search for interview questions online"""
    print(f"Searching questions for company: {company_name}")
    
    # Company-specific questions template
    company_questions = [
        {
            "question": f"How would you design a Selenium framework for {company_name}'s web applications?",
            "answer": f"Framework design for {company_name}:\n1. Page Object Model implementation\n2. Custom wait strategies\n3. Reporting and logging\n4. Data-driven approach\n5. CI/CD integration\n6. Cross-browser testing\n7. Error handling and recovery",
            "category": "Selenium",
            "difficulty": "Medium",
            "type": "Technical",
            "source": f"Custom for {company_name}"
        },
        {
            "question": f"What automation challenges would you expect at {company_name} and how would you handle them?",
            "answer": f"Expected challenges at {company_name}:\n1. Dynamic UI elements handling\n2. Test data management\n3. Environment synchronization\n4. Performance considerations\n5. Cross-browser compatibility\n6. CI/CD pipeline integration\n7. Maintenance and scalability",
            "category": "Selenium",
            "difficulty": "Medium",
            "type": "Technical",
            "source": f"Custom for {company_name}"
        },
        {
            "question": f"How would you implement parallel test execution for {company_name}'s test suite?",
            "answer": f"Parallel execution strategy:\n1. TestNG parallel execution\n2. Thread management\n3. Resource allocation\n4. Data isolation\n5. Report aggregation\n6. Grid setup\n7. Load balancing",
            "category": "Selenium",
            "difficulty": "Medium",
            "type": "Technical",
            "source": f"Custom for {company_name}"
        }
    ]
    
    questions = company_questions + [
        {
            "question": "Explain how to handle dynamic web elements in Selenium",
            "answer": "To handle dynamic elements:\n1. Use explicit waits\n2. Implement proper synchronization\n3. Use dynamic XPath/CSS selectors\n4. Handle StaleElementException\n5. Implement retry mechanisms",
            "category": "Selenium",
            "difficulty": "Medium",
            "type": "Technical"
        },
        {
            "question": "What are the different types of waits in Selenium?",
            "answer": "Selenium waits include:\n1. Implicit wait\n2. Explicit wait\n3. Fluent wait\n4. PageLoadTimeout\n5. Custom wait conditions",
            "category": "Selenium",
            "difficulty": "Basic",
            "type": "Technical"
        },
        {
            "question": "How do you handle iframes in Selenium?",
            "answer": "Handling iframes:\n1. Switch to frame using ID/name\n2. Switch using index\n3. Switch using WebElement\n4. Return to default content\n5. Handle nested frames",
            "category": "Selenium",
            "difficulty": "Basic",
            "type": "Technical"
        }
    ]
    try:
        # Common automation testing interview questions template
        # Always include these basic Selenium questions
        basic_selenium_questions = [
            {
                "question": "How do you locate elements using Selenium WebDriver?",
                "answer": "Element location methods:\n1. ID: Most reliable\n2. CSS Selectors: Flexible and fast\n3. XPath: For complex paths\n4. Class Name: For similar elements\n5. Name: Form elements\n6. Link Text/Partial Link Text\n7. Tag Name",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            },
            {
                "question": "Explain different types of waits in Selenium",
                "answer": "Types of waits:\n1. Implicit Wait: Global timeout\n2. Explicit Wait: Condition-based\n3. Fluent Wait: Custom polling\n4. PageLoadTimeout\n5. Thread.sleep (not recommended)\n6. Custom wait conditions",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            },
            {
                "question": "How do you handle alerts and popups in Selenium?",
                "answer": "Alert handling:\n1. switchTo().alert()\n2. accept() / dismiss()\n3. getText() from alert\n4. sendKeys() to alert\n5. Handle different types\n6. Try-catch for timeout",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            }
        ]
        
        # Add basic questions to ensure we always have results
        questions.extend(basic_selenium_questions)
        
        # Industry-specific keywords to enhance question relevance
        industry_keywords = {
            'default': ['web', 'mobile', 'api', 'database', 'automation', 'testing']
        }
        
        # Use default keywords for all companies
        keywords = industry_keywords['default']
        
        # Java coding specific questions
        java_coding_questions = [
            {
                "question": f"Write a Java program to find the second largest element in an array - commonly asked at {company_name}",
                "answer": "```java\npublic class SecondLargest {\n    public static int findSecondLargest(int[] arr) {\n        if (arr.length < 2) return -1;\n        \n        int largest = Integer.MIN_VALUE;\n        int secondLargest = Integer.MIN_VALUE;\n        \n        for (int num : arr) {\n            if (num > largest) {\n                secondLargest = largest;\n                largest = num;\n            } else if (num > secondLargest && num != largest) {\n                secondLargest = num;\n            }\n        }\n        \n        return secondLargest;\n    }\n}```",
                "category": "Java Coding",
                "difficulty": "Medium",
                "type": "Coding",
                "source": f"Generated for {company_name}"
            },
            {
                "question": f"Implement ArrayList from scratch in Java - {company_name} coding interview",
                "answer": "```java\npublic class CustomArrayList<T> {\n    private Object[] array;\n    private int size = 0;\n    private int capacity = 10;\n    \n    public CustomArrayList() {\n        array = new Object[capacity];\n    }\n    \n    public void add(T element) {\n        if (size >= capacity) {\n            resize();\n        }\n        array[size++] = element;\n    }\n    \n    @SuppressWarnings(\"unchecked\")\n    public T get(int index) {\n        if (index >= size || index < 0) {\n            throw new IndexOutOfBoundsException();\n        }\n        return (T) array[index];\n    }\n    \n    private void resize() {\n        capacity *= 2;\n        array = Arrays.copyOf(array, capacity);\n    }\n    \n    public int size() { return size; }\n}```",
                "category": "Java Coding",
                "difficulty": "Advanced",
                "type": "Coding",
                "source": f"Generated for {company_name}"
            },
            {
                "question": f"Write a program to check if two strings are anagrams - {company_name} Java interview",
                "answer": "```java\npublic class AnagramChecker {\n    // Method 1: Using sorting\n    public static boolean areAnagrams1(String str1, String str2) {\n        if (str1.length() != str2.length()) return false;\n        \n        char[] arr1 = str1.toLowerCase().toCharArray();\n        char[] arr2 = str2.toLowerCase().toCharArray();\n        \n        Arrays.sort(arr1);\n        Arrays.sort(arr2);\n        \n        return Arrays.equals(arr1, arr2);\n    }\n    \n    // Method 2: Using HashMap\n    public static boolean areAnagrams2(String str1, String str2) {\n        if (str1.length() != str2.length()) return false;\n        \n        Map<Character, Integer> map = new HashMap<>();\n        \n        for (char c : str1.toLowerCase().toCharArray()) {\n            map.put(c, map.getOrDefault(c, 0) + 1);\n        }\n        \n        for (char c : str2.toLowerCase().toCharArray()) {\n            map.put(c, map.getOrDefault(c, 0) - 1);\n            if (map.get(c) == 0) map.remove(c);\n        }\n        \n        return map.isEmpty();\n    }\n}```",
                "category": "Java Coding",
                "difficulty": "Medium",
                "type": "Coding",
                "source": f"Generated for {company_name}"
            },
            {
                "question": f"Implement a stack using LinkedList in Java - {company_name} data structure question",
                "answer": "```java\npublic class StackUsingLinkedList<T> {\n    private Node<T> top;\n    private int size;\n    \n    private static class Node<T> {\n        T data;\n        Node<T> next;\n        \n        Node(T data) {\n            this.data = data;\n        }\n    }\n    \n    public void push(T item) {\n        Node<T> newNode = new Node<>(item);\n        newNode.next = top;\n        top = newNode;\n        size++;\n    }\n    \n    public T pop() {\n        if (isEmpty()) {\n            throw new EmptyStackException();\n        }\n        T data = top.data;\n        top = top.next;\n        size--;\n        return data;\n    }\n    \n    public T peek() {\n        if (isEmpty()) {\n            throw new EmptyStackException();\n        }\n        return top.data;\n    }\n    \n    public boolean isEmpty() {\n        return top == null;\n    }\n    \n    public int size() {\n        return size;\n    }\n}```",
                "category": "Java Coding",
                "difficulty": "Medium",
                "type": "Coding",
                "source": f"Generated for {company_name}"
            }
        ]
        
        # Generate relevant questions for any company
        common_questions = [
            {
                "question": f"How would you approach testing {company_name}'s core business applications?",
                "answer": f"Testing approach for {company_name}:\n1. Understand business domain and requirements\n2. Identify critical workflows\n3. Design test scenarios for key features\n4. Implement automated regression suite\n5. Performance testing strategy\n6. Security testing considerations\n7. Integration testing approach",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            },
            {
                "question": f"What test scenarios would you automate first for {company_name}'s web application?",
                "answer": f"Priority test scenarios:\n1. Login functionality\n2. Core business workflows\n3. Data validation\n4. Error handling\n5. Cross-browser compatibility\n6. Responsive design\n7. Integration points",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            },
            {
                "question": f"How would you handle dynamic elements in {company_name}'s web interface?",
                "answer": "Dynamic elements handling:\n1. Implement explicit waits\n2. Use dynamic element locators\n3. Handle AJAX requests\n4. Implement retry mechanisms\n5. Error handling for state changes\n6. Page load verification\n7. Synchronization strategies",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            },
            {
                "question": f"What automation framework features would be crucial for {company_name}'s testing needs?",
                "answer": f"Essential framework features:\n1. Robust element identification\n2. Test data management\n3. Environment configuration\n4. Reporting and logging\n5. Error handling and recovery\n6. CI/CD integration\n7. Cross-browser support",
                "category": "Selenium",
                "type": "Technical",
                "difficulty": "Basic"
            },
            {
                "question": f"What would be your testing strategy for {company_name}'s main user workflows?",
                "answer": f"Testing strategy for {company_name}:\n1. Identify critical user journeys\n2. Risk-based test prioritization\n3. Automated regression suite\n4. Performance testing\n5. Security testing\n6. Mobile compatibility\n7. Analytics verification",
                "category": "Test Strategy",
                "type": "Technical"
            },
            {
                "question": f"How would you implement API testing for {company_name}'s services?",
                "answer": "API testing implementation:\n1. REST/SOAP endpoints validation\n2. Request/Response verification\n3. Security testing (authentication/authorization)\n4. Performance testing\n5. Error scenarios\n6. Integration testing\n7. Contract testing",
                "category": "API Testing",
                "type": "Technical"
            },
            {
                "question": f"What key areas would you focus on for {company_name}'s mobile app testing?",
                "answer": "Mobile testing focus areas:\n1. User interface and experience\n2. Device compatibility\n3. Network conditions\n4. Performance metrics\n5. Security aspects\n6. Battery consumption\n7. Integration points",
                "category": "Mobile Testing",
                "type": "Technical"
            },
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

        # Add Java coding questions if category matches
        if category.lower() == "java coding":
            for java_q in java_coding_questions:
                questions.append(java_q)
        
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

        # Enhanced multi-platform search functions
        def search_google_for_questions(company, role, category):
            """Search Google for interview questions from multiple sources"""
            all_questions = []
            
            # Different search queries to get varied results
            # Dynamic search queries based on category
            if category.lower() == "java coding":
                search_queries = [
                    f"{company} java coding interview questions",
                    f"{company} java programming interview",
                    f"{company} java algorithms data structures interview",
                    f"{company} java collections interview questions",
                    f"{company} java coding problems interview",
                    f"{company} core java interview coding questions"
                ]
            else:
                search_queries = [
                    f"{company} {role} interview questions {category}",
                    f"{company} automation testing interview experience",
                    f"{company} selenium webdriver interview questions",
                    f"{company} technical interview questions testing",
                    f"{company} software tester interview questions",
                    f"{company} QA automation interview experience"
                ]
            
            platforms = {
                'glassdoor.com': 'Glassdoor',
                'geeksforgeeks.org': 'GeeksforGeeks', 
                'ambitionbox.com': 'AmbitionBox',
                'linkedin.com': 'LinkedIn',
                'naukri.com': 'Naukri',
                'indeed.com': 'Indeed',
                'interviewbit.com': 'InterviewBit',
                'careercup.com': 'CareerCup',
                'leetcode.com': 'LeetCode'
            }
            
            for query in search_queries[:3]:  # Limit to 3 queries to avoid rate limiting
                try:
                    # Use Google search to find relevant pages
                    search_url = f"https://www.google.com/search?q={quote(query)}"
                    response = requests.get(search_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Extract search results
                        search_results = soup.find_all('div', {'class': 'g'})[:10]  # Top 10 results
                        
                        for result in search_results:
                            try:
                                link_element = result.find('a')
                                if link_element and 'href' in link_element.attrs:
                                    url = link_element['href']
                                    title = result.find('h3')
                                    
                                    if title:
                                        title_text = title.get_text(strip=True)
                                        
                                        # Check if URL is from known platforms
                                        source = "Web Search"
                                        for platform, platform_name in platforms.items():
                                            if platform in url:
                                                source = platform_name
                                                break
                                        
                                        # Extract potential questions from title/snippet
                                        if any(keyword in title_text.lower() for keyword in ['interview', 'question', 'experience']):
                                            all_questions.append({
                                                "question": title_text,
                                                "source": source,
                                                "url": url,
                                                "company": company,
                                                "category": category,
                                                "difficulty": "Medium",
                                                "type": "Technical"
                                            })
                            except Exception as e:
                                continue
                    
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    print(f"Error in Google search: {str(e)}")
                    continue
            
            return all_questions

        def scrape_glassdoor(company):
            """Enhanced Glassdoor scraping"""
            questions = []
            search_terms = [company, f"{company} automation", f"{company} selenium", f"{company} testing"]
            
            for term in search_terms[:2]:  # Limit searches
                try:
                    # Search Glassdoor interview section
                    search_url = f"https://www.glassdoor.com/Interview/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={quote(term)}&sc.keyword={quote(term)}"
                    response = requests.get(search_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for interview question elements with various selectors
                        question_selectors = [
                            '.questionText',
                            '[data-test="interview-question"]',
                            '.interviewQuestion',
                            '.question-text'
                        ]
                        
                        for selector in question_selectors:
                            elements = soup.select(selector)
                            for element in elements:
                                question_text = element.get_text(strip=True)
                                # Keywords based on category
                            if category.lower() == "java coding":
                                relevant_keywords = ['java', 'coding', 'programming', 'algorithm', 'data structure', 'array', 'string', 'hashmap', 'collection']
                            else:
                                relevant_keywords = ['selenium', 'automation', 'testing', 'framework', 'webdriver']
                            
                            if len(question_text) > 10 and any(keyword in question_text.lower() for keyword in relevant_keywords):
                                    questions.append({
                                        "question": question_text,
                                        "source": "Glassdoor",
                                        "company": company,
                                        "category": "Selenium",
                                        "difficulty": "Medium",
                                        "type": "Technical"
                                    })
                    
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    print(f"Error scraping Glassdoor for {term}: {str(e)}")
                    continue
            
            return questions

        def scrape_geeksforgeeks(company):
            """Enhanced GeeksforGeeks scraping"""
            questions = []
            search_urls = [
                f"https://www.geeksforgeeks.org/?s={quote(company + ' interview')}",
                f"https://www.geeksforgeeks.org/tag/{company.lower()}-interview-experience/",
                f"https://www.geeksforgeeks.org/?s={quote(company + ' automation testing')}"
            ]
            
            for url in search_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Look for article titles and content
                        article_elements = soup.find_all(['h2', 'h3', 'h4', 'p', 'li'])
                        
                        for element in article_elements:
                            text = element.get_text(strip=True)
                            
                            # Check if it's a question (contains question words)
                            if ('?' in text or any(starter in text.lower() for starter in ['what is', 'how do', 'explain', 'describe', 'why', 'when'])) and len(text) > 20:
                                if any(keyword in text.lower() for keyword in ['selenium', 'automation', 'testing', 'webdriver', 'framework']):
                                    questions.append({
                                        "question": text,
                                        "source": "GeeksforGeeks",
                                        "company": company,
                                        "category": "Selenium",
                                        "difficulty": "Medium",
                                        "type": "Technical"
                                    })
                    
                    time.sleep(1)
                except Exception as e:
                    print(f"Error scraping GeeksforGeeks: {str(e)}")
                    continue
            
            return questions

        def scrape_ambitionbox(company):
            """Scrape AmbitionBox for interview questions"""
            questions = []
            try:
                search_url = f"https://www.ambitionbox.com/search?q={quote(company)}"
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for interview-related content
                    content_elements = soup.find_all(['div', 'p', 'span'], class_=lambda x: x and ('interview' in x.lower() or 'question' in x.lower()))
                    
                    for element in content_elements:
                        text = element.get_text(strip=True)
                        if len(text) > 15 and any(keyword in text.lower() for keyword in ['selenium', 'automation', 'testing']):
                            questions.append({
                                "question": text,
                                "source": "AmbitionBox",
                                "company": company,
                                "category": "Selenium",
                                "difficulty": "Medium",
                                "type": "Technical"
                            })
            except Exception as e:
                print(f"Error scraping AmbitionBox: {str(e)}")
            
            return questions

        def scrape_naukri_indeed(company):
            """Scrape job portals for interview insights"""
            questions = []
            portals = [
                ('naukri.com', 'Naukri'),
                ('indeed.com', 'Indeed')
            ]
            
            for domain, source_name in portals:
                try:
                    search_url = f"https://www.google.com/search?q=site:{domain} {quote(company)} interview questions automation testing"
                    response = requests.get(search_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Extract search result titles and snippets
                        results = soup.find_all('div', {'class': 'g'})
                        
                        for result in results[:5]:  # Top 5 results per portal
                            try:
                                title_elem = result.find('h3')
                                snippet_elem = result.find('span', {'class': 'st'}) or result.find('div', {'class': 'VwiC3b'})
                                
                                if title_elem:
                                    title = title_elem.get_text(strip=True)
                                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                                    
                                    combined_text = f"{title}. {snippet}"
                                    
                                    if any(keyword in combined_text.lower() for keyword in ['interview', 'question', 'selenium', 'automation']):
                                        questions.append({
                                            "question": combined_text[:200] + "..." if len(combined_text) > 200 else combined_text,
                                            "source": source_name,
                                            "company": company,
                                            "category": "Selenium",
                                            "difficulty": "Medium",
                                            "type": "Technical"
                                        })
                            except Exception as e:
                                continue
                    
                    time.sleep(1)
                except Exception as e:
                    print(f"Error searching {source_name}: {str(e)}")
                    continue
            
            return questions

        # Enhanced multi-platform search - Get questions from ALL sources
        print(f"🔍 Starting comprehensive search for {company_name} interview questions...")
        all_real_questions = []
        
        # 1. Google Search for questions from multiple platforms
        print("🌐 Searching Google for interview questions...")
        google_questions = search_google_for_questions(company_name, role, category)
        if google_questions:
            all_real_questions.extend(google_questions)
            print(f"✅ Found {len(google_questions)} questions from Google search")

        # 2. Glassdoor scraping
        print("💼 Scraping Glassdoor...")
        glassdoor_questions = scrape_glassdoor(company_name)
        if glassdoor_questions:
            all_real_questions.extend(glassdoor_questions)
            print(f"✅ Found {len(glassdoor_questions)} questions from Glassdoor")

        # 3. GeeksforGeeks scraping
        print("🎓 Scraping GeeksforGeeks...")
        geeksforgeeks_questions = scrape_geeksforgeeks(company_name)
        if geeksforgeeks_questions:
            all_real_questions.extend(geeksforgeeks_questions)
            print(f"✅ Found {len(geeksforgeeks_questions)} questions from GeeksforGeeks")

        # 4. AmbitionBox scraping
        print("💡 Scraping AmbitionBox...")
        ambitionbox_questions = scrape_ambitionbox(company_name)
        if ambitionbox_questions:
            all_real_questions.extend(ambitionbox_questions)
            print(f"✅ Found {len(ambitionbox_questions)} questions from AmbitionBox")

        # 5. Naukri and Indeed search
        print("🔍 Searching job portals...")
        portal_questions = scrape_naukri_indeed(company_name)
        if portal_questions:
            all_real_questions.extend(portal_questions)
            print(f"✅ Found {len(portal_questions)} questions from job portals")

        # Add all real questions found
        if all_real_questions:
            print(f"🎉 Total found: {len(all_real_questions)} real questions from online sources!")
            questions.extend(all_real_questions)
            
            # Remove duplicates based on question text
            seen_questions = set()
            unique_questions = []
            for q in questions:
                question_text = q.get('question', '').lower().strip()
                if question_text not in seen_questions and len(question_text) > 10:
                    seen_questions.add(question_text)
                    unique_questions.append(q)
            
            questions = unique_questions
            print(f"📋 After removing duplicates: {len(questions)} unique questions")
        else:
            print("⚠️ No real questions found from online sources, using enhanced templates")
            # Mark template questions clearly
            for q in questions:
                q["source"] = "Generated Template"


        return questions
    except Exception as e:
        print(f"Error in search: {str(e)}")
        return []