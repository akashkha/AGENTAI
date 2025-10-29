import json
import os
try:
    from .interview_bot import InterviewBot
except ImportError:
    from interview_bot import InterviewBot
from datetime import datetime

class ChatBot:
    def __init__(self):
        self.bot = InterviewBot()
        self.context = {}
        self.conversation_history = []
        
    def save_conversation(self):
        """Save conversation history to a file"""
        if not os.path.exists('chat_history'):
            os.makedirs('chat_history')
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'chat_history/conversation_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
            
    def process_message(self, message):
        """Process user message and return response"""
        message = message.lower().strip()
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Initial greeting
        if any(greeting in message for greeting in ['hi', 'hello', 'hey']):
            response = (
                "Hello! I'm your Interview Preparation Assistant. I can help you with:\n"
                "1. Finding interview questions for specific companies\n"
                "2. Questions by experience level\n"
                "3. Questions by category (like Selenium, API Testing, etc.)\n"
                "4. Questions by difficulty level\n"
                "5. Coding practice questions\n\n"
                "What would you like to know about?"
            )
            
        # Company specific questions
        elif "questions" in message and any(company.lower() in message for company in self.bot.get_available_companies()):
            company = next(c for c in self.bot.get_available_companies() if c.lower() in message.lower())
            
            # Try to extract experience from message
            experience = "2"  # default
            for word in message.split():
                if word.replace('.', '').isdigit():
                    experience = word
                    break
                    
            response = self.bot.format_response(
                self.bot.get_interview_questions(company, experience)
            )
            
        # Show categories
        elif "categories" in message or "topics" in message:
            categories = self.bot.get_categories()
            if not categories:
                response = "Sorry, I couldn't load the categories. Please try again."
            else:
                response = "Here are the available categories and their topics:\n\n"
                for category, topics in categories.items():
                    response += f"{category}:\n"
                    for topic in topics:
                        response += f"  - {topic}\n"
                    
        # Show companies
        elif "companies" in message:
            companies = self.bot.get_available_companies()
            response = "Here are the companies I have questions for:\n\n"
            response += "\n".join(f"- {company}" for company in companies)
        # Handle coding questions
        elif "coding" in message:
            if "categories" in message:
                categories = self.bot.get_coding_categories()
                response = "Available coding question categories:\n\n"
                response += "\n".join(f"- {category}" for category in categories)
            elif any(category.lower() in message for category in self.bot.get_coding_categories()):
                category = next(c for c in self.bot.get_coding_categories() if c.lower() in message.lower())
                difficulties = self.bot.get_coding_difficulties(category)
                if "easy" in message.lower():
                    difficulty = "Easy"
                elif "medium" in message.lower():
                    difficulty = "Medium"
                elif "hard" in message.lower():
                    difficulty = "Hard"
                else:
                    response = f"Available difficulty levels for {category}:\n\n"
                    response += "\n".join(f"- {diff}" for diff in difficulties)
                    return response

                question = self.bot.get_coding_question(category, difficulty)
                if question:
                    response = (
                        f"Here's a {difficulty} {category} coding question:\n\n"
                        f"Question: {question['question']}\n\n"
                        f"Template:\n```python\n{question['code_template']}\n```\n\n"
                        f"Hints:\n" + "\n".join(f"- {hint}" for hint in question['hints']) + "\n\n"
                        f"Test Cases:\n" + "\n".join(f"- {test}" for test in question['test_cases']) + "\n\n"
                        f"Type 'solution' to see the solution."
                    )
                    # Store the current question in context for showing solution later
                    self.context['current_question'] = question
                else:
                    response = f"No {difficulty} questions found for {category}."
            else:
                categories = self.bot.get_coding_categories()
                response = (
                    "I have coding practice questions in these categories:\n\n" +
                    "\n".join(f"- {category}" for category in categories) +
                    "\n\nYou can ask for questions by category and difficulty, e.g.:\n" +
                    "'Show me an easy Automation coding question' or\n" +
                    "'Give me a hard DSA question'"
                )
<<<<<<< HEAD
        
=======

>>>>>>> 4f8dd752c6b6d73acc9ce3a04eb8b1f91cbcdfd8
        # Show solution for current coding question
        elif ("solution" in message or "approach" in message or "another" in message) and 'current_question' in self.context:
            question = self.context['current_question']
            if "another" in message or "alternative" in message or "different" in message:
                if 'alternative_solutions' in question:
                    alt_solutions = question['alternative_solutions']
                    response = f"Here are alternative approaches for: {question['question']}\n\n"
                    for i, sol in enumerate(alt_solutions, 1):
                        response += f"Approach #{i}: {sol['description']}\n"
                        response += f"```python\n{sol['code']}\n```\n\n"
                else:
                    # Search internet for alternative solutions
                    search_results = self.bot.search_internet(f"alternative solution {question['question']}")
                    if search_results:
                        response = f"Here are some alternative approaches I found online:\n\n{search_results}"
                    else:
                        response = "Sorry, I couldn't find any alternative solutions at the moment."
            else:
                response = (
                    f"Solution for: {question['question']}\n\n"
                    f"```python\n{question['solution']}\n```"
                )

        # Help message
        elif "help" in message:
            response = (
                "Here's how you can interact with me:\n\n"
                "Interview Questions:\n"
                "- Ask for questions: 'Show me TCS interview questions for 2 years experience'\n"
                "- View categories: 'What categories of questions do you have?'\n"
                "- List companies: 'Which companies do you have questions for?'\n"
                "- Get specific: 'Show me Selenium questions for Microsoft'\n"
                "- Filter by difficulty: 'Show me advanced questions for Amazon'\n\n"
                "Coding Practice:\n"
                "- View coding categories: 'What coding categories do you have?'\n"
                "- Get coding questions: 'Show me an easy Automation coding question'\n"
                "- View solutions: Type 'solution' after getting a coding question\n\n"
                "You can combine filters: 'Show me advanced Selenium questions for TCS with 3 years experience'"
            )
            
        # Goodbye
        elif any(word in message for word in ['bye', 'goodbye', 'exit', 'quit']):
            self.save_conversation()
            response = "Thank you for using the Interview Bot! Your conversation has been saved. Good luck with your interview preparation!"
            
        # Default response - try internet search for technical queries
        else:
            # Identify question type and category
            query_categories = {
                'technical': ['how to', 'what is', 'explain', 'difference between', 'example', 'code', 'programming',
                            'function', 'class', 'implement', 'python', 'java', 'javascript', 'selenium', 'api', 'test'],
                'behavioral': ['tell me about', 'how did you', 'describe', 'situation', 'challenge', 'conflict',
                             'difficult', 'team', 'leadership', 'achievement', 'mistake', 'pressure', 'deadline'],
                'system_design': ['design', 'architecture', 'scale', 'database', 'system', 'infrastructure',
                                'microservice', 'distributed', 'cloud', 'performance', 'optimization'],
                'hr': ['salary', 'notice', 'joining', 'relocation', 'package', 'benefits', 'work culture',
                      'company values', 'career growth', 'expectations', 'why join', 'why leave']
            }
            
            # Determine category
            message_lower = message.lower()
            category = None
            for cat, keywords in query_categories.items():
                if any(keyword in message_lower for keyword in keywords):
                    category = cat
                    break
            
            # Search for answer
            if category or 'interview' in message_lower or 'question' in message_lower:
                search_results = self.bot.search_internet(message, category)
                if search_results:
                    response = f"Here's what I found:\n\n{search_results}"
                else:
                    response = (
                        "I couldn't find specific information for your query. You can:\n"
                        "- Ask for company specific questions\n"
                        "- View question categories\n"
                        "- List available companies\n"
                        "- Type 'help' for more details\n"
                    )
            else:
                response = (
                    "I'm not sure I understood that. You can:\n"
                    "- Ask for company specific questions\n"
                    "- View question categories\n"
                    "- List available companies\n"
                    "- Type 'help' for more details\n"
                )
            
        # Add bot response to history
        self.conversation_history.append({
            "role": "bot",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response

def main():
    chat_bot = ChatBot()
    print("Welcome to the Interview Preparation Chat Bot!")
    print("Type 'help' for guidance or 'exit' to quit.")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                response = chat_bot.process_message(user_input)
                print(f"\nBot: {response}")
                break
                
            response = chat_bot.process_message(user_input)
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\n\nExiting gracefully...")
            chat_bot.save_conversation()
            break
        except Exception as e:
            print(f"\nBot: I encountered an error: {str(e)}")
            print("Let's try something else!")

if __name__ == "__main__":
    main()