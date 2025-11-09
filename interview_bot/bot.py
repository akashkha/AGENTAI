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
            
            # Initialize default questions that will always be available
            self.base_questions = [
                {
                    "question": "What are the key components of a Selenium test framework?",
                    "answer": "1. WebDriver setup and configuration\n2. Page Object Model implementation\n3. Test data management\n4. Reporting and logging\n5. Utility functions\n6. Test base classes\n7. Configuration management",
                    "category": "Selenium",
                    "difficulty": "Medium",
                    "type": "Technical",
                    "source": "Standard Interview Question"
                },
                {
                    "question": "How do you handle dynamic elements in Selenium?",
                    "answer": "1. Explicit waits with Expected Conditions\n2. Custom wait conditions\n3. JavaScript execution if needed\n4. Dynamic XPath strategies\n5. Proper synchronization mechanisms",
                    "category": "Selenium",
                    "difficulty": "Medium",
                    "type": "Technical",
                    "source": "Standard Interview Question"
                },
                {
                    "question": "Explain your approach to data-driven testing in Selenium",
                    "answer": "1. External data sources (Excel, CSV, JSON)\n2. Parameterization techniques\n3. Test data management strategies\n4. Data providers implementation\n5. Configuration handling",
                    "category": "Selenium",
                    "difficulty": "Medium",
                    "type": "Technical",
                    "source": "Standard Interview Question"
                }
            ]
            
            self.default_questions = {
                "0-2": [
                    {
                        "question": "What are the basic Selenium locators you use?",
                        "answer": "Basic Selenium locators include:\n1. ID\n2. Name\n3. Class Name\n4. Tag Name\n5. Link Text\n6. Partial Link Text\n7. CSS Selector\n8. XPath",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    },
                    {
                        "question": "How do you handle dynamic elements in Selenium?",
                        "answer": "To handle dynamic elements:\n1. Use explicit waits\n2. Implement proper synchronization\n3. Use dynamic locators\n4. Handle StaleElementException\n5. Implement retry mechanisms",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    },
                    {
                        "question": "Explain different types of waits in Selenium",
                        "answer": "Different types of waits:\n1. Implicit Wait\n2. Explicit Wait\n3. Fluent Wait\n4. PageLoadTimeout\n5. Custom wait conditions",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    },
                    {
                        "question": "What are the main components of Selenium WebDriver?",
                        "answer": "Main components:\n1. WebDriver\n2. WebElement\n3. Select class\n4. Alert interface\n5. Navigation interface\n6. Actions class\n7. JavascriptExecutor",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    },
                    {
                        "question": "How do you handle alerts and popups in Selenium?",
                        "answer": "Handling alerts:\n1. switchTo().alert()\n2. accept() method\n3. dismiss() method\n4. getText() from alert\n5. sendKeys() to alert\n6. Try-catch for timeout handling",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    },
                    {
                        "question": "What is the difference between driver.close() and driver.quit()?",
                        "answer": "Difference:\n1. close(): Closes current window only\n2. quit(): Closes all browser windows\n3. quit(): Terminates WebDriver session\n4. close(): Window handle remains valid\n5. quit(): Releases all resources",
                        "category": "Selenium",
                        "difficulty": "Basic",
                        "type": "Technical"
                    },
                    {
                        "question": "Write a Java program to check if a string is palindrome",
                        "answer": "```java\npublic class PalindromeCheck {\n    public static boolean isPalindrome(String str) {\n        str = str.toLowerCase().replaceAll(\"[^a-zA-Z0-9]\", \"\");\n        int left = 0, right = str.length() - 1;\n        \n        while (left < right) {\n            if (str.charAt(left) != str.charAt(right)) {\n                return false;\n            }\n            left++;\n            right--;\n        }\n        return true;\n    }\n    \n    public static void main(String[] args) {\n        System.out.println(isPalindrome(\"racecar\")); // true\n        System.out.println(isPalindrome(\"hello\")); // false\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Basic",
                        "type": "Coding"
                    },
                    {
                        "question": "Find the largest and smallest elements in an array using Java",
                        "answer": "```java\npublic class MinMaxFinder {\n    public static void findMinMax(int[] arr) {\n        if (arr.length == 0) return;\n        \n        int min = arr[0], max = arr[0];\n        \n        for (int i = 1; i < arr.length; i++) {\n            if (arr[i] < min) {\n                min = arr[i];\n            }\n            if (arr[i] > max) {\n                max = arr[i];\n            }\n        }\n        \n        System.out.println(\"Min: \" + min + \", Max: \" + max);\n    }\n    \n    // Using Collections\n    public static void findMinMaxWithCollections(List<Integer> list) {\n        int min = Collections.min(list);\n        int max = Collections.max(list);\n        System.out.println(\"Min: \" + min + \", Max: \" + max);\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Basic",
                        "type": "Coding"
                    },
                    {
                        "question": "Write a program to count frequency of characters in a string using HashMap",
                        "answer": "```java\nimport java.util.*;\n\npublic class CharacterFrequency {\n    public static void countCharacters(String str) {\n        Map<Character, Integer> frequencyMap = new HashMap<>();\n        \n        for (char c : str.toCharArray()) {\n            frequencyMap.put(c, frequencyMap.getOrDefault(c, 0) + 1);\n        }\n        \n        // Print frequency\n        for (Map.Entry<Character, Integer> entry : frequencyMap.entrySet()) {\n            System.out.println(entry.getKey() + \": \" + entry.getValue());\n        }\n    }\n    \n    // Using Java 8 Streams\n    public static void countWithStreams(String str) {\n        str.chars()\n           .mapToObj(c -> (char) c)\n           .collect(Collectors.groupingBy(c -> c, Collectors.counting()))\n           .forEach((k, v) -> System.out.println(k + \": \" + v));\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Basic",
                        "type": "Coding"
                    },
                    {
                        "question": "Implement bubble sort algorithm in Java",
                        "answer": "```java\npublic class BubbleSort {\n    public static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        boolean swapped;\n        \n        for (int i = 0; i < n - 1; i++) {\n            swapped = false;\n            \n            for (int j = 0; j < n - i - 1; j++) {\n                if (arr[j] > arr[j + 1]) {\n                    // Swap elements\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                    swapped = true;\n                }\n            }\n            \n            // If no swapping occurred, array is sorted\n            if (!swapped) break;\n        }\n    }\n    \n    public static void printArray(int[] arr) {\n        System.out.println(Arrays.toString(arr));\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Basic",
                        "type": "Coding"
                    }
                ],
                "2-5": [
                    {
                        "question": "How do you implement Page Object Model?",
                        "answer": "Implementing POM:\n1. Create separate class for each page\n2. Define elements as private variables\n3. Create public methods for actions\n4. Use proper encapsulation\n5. Implement reusable methods",
                        "category": "Selenium",
                        "difficulty": "Medium",
                        "type": "Technical"
                    },
                    {
                        "question": "How do you handle iframes in Selenium?",
                        "answer": "Handling iframes:\n1. Switch to frame using ID/Name\n2. Switch using index\n3. Switch using WebElement\n4. Return to default content\n5. Handle nested frames",
                        "category": "Selenium",
                        "difficulty": "Medium",
                        "type": "Technical"
                    },
                    {
                        "question": "How do you implement data-driven testing in Selenium?",
                        "answer": "Data-driven implementation:\n1. External data sources (Excel, CSV, JSON)\n2. TestNG DataProvider\n3. Parameterized tests\n4. Test data management\n5. Configuration handling\n6. Database integration\n7. API data sources",
                        "category": "Selenium",
                        "difficulty": "Medium",
                        "type": "Technical"
                    },
                    {
                        "question": "Explain TestNG annotations and their execution order",
                        "answer": "TestNG annotations:\n1. @BeforeSuite\n2. @BeforeTest\n3. @BeforeClass\n4. @BeforeMethod\n5. @Test\n6. @AfterMethod\n7. @AfterClass\n8. @AfterTest\n9. @AfterSuite",
                        "category": "TestNG",
                        "difficulty": "Medium",
                        "type": "Technical"
                    },
                    {
                        "question": "How do you handle cross-browser testing in your framework?",
                        "answer": "Cross-browser testing:\n1. Driver factory pattern\n2. Browser configuration\n3. Selenium Grid setup\n4. Cloud services integration\n5. Parallel execution\n6. Browser-specific handling\n7. Compatibility testing",
                        "category": "Framework Design",
                        "difficulty": "Medium",
                        "type": "Technical"
                    },
                    {
                        "question": "How do you implement reporting in your automation framework?",
                        "answer": "Reporting implementation:\n1. ExtentReports integration\n2. TestNG listeners\n3. Screenshot capture\n4. Log management\n5. HTML reports\n6. Email notifications\n7. Dashboard integration",
                        "category": "Framework Design",
                        "difficulty": "Medium",
                        "type": "Technical"
                    },
                    {
                        "question": "Write a Java program to find duplicate elements in an array",
                        "answer": "```java\npublic class FindDuplicates {\n    public static void findDuplicates(int[] arr) {\n        Set<Integer> seen = new HashSet<>();\n        Set<Integer> duplicates = new HashSet<>();\n        \n        for (int num : arr) {\n            if (!seen.add(num)) {\n                duplicates.add(num);\n            }\n        }\n        \n        System.out.println(\"Duplicates: \" + duplicates);\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Medium",
                        "type": "Coding"
                    },
                    {
                        "question": "How to reverse a string in Java without using built-in methods?",
                        "answer": "```java\npublic class ReverseString {\n    public static String reverse(String str) {\n        char[] chars = str.toCharArray();\n        int left = 0, right = chars.length - 1;\n        \n        while (left < right) {\n            char temp = chars[left];\n            chars[left] = chars[right];\n            chars[right] = temp;\n            left++;\n            right--;\n        }\n        \n        return new String(chars);\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Basic",
                        "type": "Coding"
                    }
                ]
            }
            
            # Extend default_questions with additional experience-based questions
            self.default_questions["5+"] = [
                {
                    "question": "How do you design a scalable automation framework architecture?",
                    "answer": "Scalable architecture design:\n1. Modular framework design\n2. Microservices testing approach\n3. Cloud-based execution\n4. Advanced reporting systems\n5. Performance optimization\n6. Team collaboration tools\n7. Maintenance strategies",
                    "category": "Selenium",
                    "difficulty": "Advanced",
                    "type": "Technical"
                },
                {
                    "question": "How do you implement CI/CD pipeline integration for automation tests?",
                    "answer": "CI/CD integration:\n1. Jenkins/Azure DevOps setup\n2. Automated test execution triggers\n3. Parallel execution strategies\n4. Test result reporting\n5. Failure analysis automation\n6. Environment management\n7. Deployment validation",
                        "category": "Selenium", 
                        "difficulty": "Advanced",
                        "type": "Technical"
                    },
                    {
                        "question": "Implement a custom HashMap in Java with collision handling",
                        "answer": "```java\npublic class CustomHashMap<K, V> {\n    private Node<K, V>[] buckets;\n    private int capacity = 16;\n    private int size = 0;\n    \n    static class Node<K, V> {\n        K key;\n        V value;\n        Node<K, V> next;\n        \n        Node(K key, V value) {\n            this.key = key;\n            this.value = value;\n        }\n    }\n    \n    public CustomHashMap() {\n        buckets = new Node[capacity];\n    }\n    \n    private int hash(K key) {\n        return Math.abs(key.hashCode() % capacity);\n    }\n    \n    public void put(K key, V value) {\n        int index = hash(key);\n        Node<K, V> head = buckets[index];\n        \n        // Check if key already exists\n        Node<K, V> current = head;\n        while (current != null) {\n            if (current.key.equals(key)) {\n                current.value = value;\n                return;\n            }\n            current = current.next;\n        }\n        \n        // Add new node\n        Node<K, V> newNode = new Node<>(key, value);\n        newNode.next = head;\n        buckets[index] = newNode;\n        size++;\n    }\n    \n    public V get(K key) {\n        int index = hash(key);\n        Node<K, V> head = buckets[index];\n        \n        while (head != null) {\n            if (head.key.equals(key)) {\n                return head.value;\n            }\n            head = head.next;\n        }\n        return null;\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Advanced", 
                        "type": "Coding"
                    },
                    {
                        "question": "Design and implement a thread-safe Singleton pattern in Java",
                        "answer": "```java\npublic class ThreadSafeSingleton {\n    private static volatile ThreadSafeSingleton instance;\n    \n    private ThreadSafeSingleton() {\n        // Private constructor\n    }\n    \n    // Double-checked locking\n    public static ThreadSafeSingleton getInstance() {\n        if (instance == null) {\n            synchronized (ThreadSafeSingleton.class) {\n                if (instance == null) {\n                    instance = new ThreadSafeSingleton();\n                }\n            }\n        }\n        return instance;\n    }\n    \n    // Bill Pugh Solution (Recommended)\n    private static class SingletonHelper {\n        private static final ThreadSafeSingleton INSTANCE = new ThreadSafeSingleton();\n    }\n    \n    public static ThreadSafeSingleton getBillPughInstance() {\n        return SingletonHelper.INSTANCE;\n    }\n}```",
                        "category": "Java Coding",
                        "difficulty": "Advanced",
                        "type": "Coding"
                    }
                ]            # Look for questions_db.json in the interview_bot package directory
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
            if not company or not isinstance(company, str):
                return {"status": "error", "message": "Please provide a valid company name."}
            
            print("Debug: Starting question retrieval...")
            
            # Always start with base questions
            questions = self.base_questions.copy()
            
            company = company.strip()
            exp_range = self.get_experience_range(years_of_experience)
            questions = []
            
            # Start with default questions for the experience range
            questions.extend(self.default_questions.get(exp_range, []))
            
            # Get company-specific questions if they exist
            if company in self.questions_db.get("companies", {}):
                company_questions = self.questions_db["companies"][company].get(exp_range, [])
                questions.extend(company_questions)
            
            # Get comprehensive web search results from all platforms
            print(f"🚀 Starting comprehensive search for {company} interview questions...")
            web_results = search_interview_questions(
                company, 
                role="automation tester", 
                category=category or "selenium", 
                max_questions=100  # Get up to 100 questions from web
            )
            
            print(f"📊 Web search returned {len(web_results)} questions")
            for q in web_results:
                q["experience_range"] = exp_range
                # Add all web results - no filtering by company name to get more variety
                questions.append(q)
            
            # Ensure all questions have proper metadata
            for q in questions:
                if not q.get("category"):
                    q["category"] = "Selenium"
                if not q.get("difficulty"):
                    q["difficulty"] = "Basic"
                if not q.get("type"):
                    q["type"] = "Technical"
                q["experience_range"] = exp_range
            
            # Keep track of original questions before filtering
            all_questions = questions.copy()
            
            # Apply filters if specified
            print(f"Debug: Before filtering - {len(questions)} questions")
            
            if category and category != "All":
                filtered = [q for q in questions if q.get("category", "Selenium") == category]
                print(f"Debug: After category filter - {len(filtered)} questions")
                if filtered:
                    questions = filtered
            
            if difficulty and difficulty != "All":
                filtered = [q for q in questions if q.get("difficulty", "Medium") == difficulty]
                print(f"Debug: After difficulty filter - {len(filtered)} questions")
                if filtered:
                    questions = filtered
            
            # If no questions match filters, return the original set
            if not questions:
                print("Debug: No questions after filtering, restoring original set")
                questions = all_questions
            
            # Ensure questions are unique
            seen = set()
            unique_questions = []
            for q in questions:
                q_text = q.get("question", "")
                if q_text not in seen:
                    seen.add(q_text)
                    unique_questions.append(q)
            questions = unique_questions
            
            print(f"Returning {len(questions)} questions")
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