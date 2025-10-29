from flask import Flask, render_template, request, jsonify
from interview_bot import InterviewBot
import os

app = Flask(__name__)
bot = InterviewBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        # Process the message using our existing bot logic
        response = process_message(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_message(message):
    message = message.lower().strip()
    
    # Initial greeting
    if any(greeting in message for greeting in ['hi', 'hello', 'hey']):
        return {
            "type": "text",
            "content": (
                "Hello! I'm your Interview Preparation Assistant. I can help you with:\n"
                "1. Finding interview questions for specific companies\n"
                "2. Questions by experience level\n"
                "3. Questions by category (like Selenium, API Testing, etc.)\n"
                "4. Questions by difficulty level\n\n"
                "What would you like to know about?"
            )
        }
    
    # Company specific questions
    elif "questions" in message and any(company.lower() in message for company in bot.get_available_companies()):
        company = next(c for c in bot.get_available_companies() if c.lower() in message.lower())
        
        # Try to extract experience from message
        experience = "2"  # default
        for word in message.split():
            if word.replace('.', '').isdigit():
                experience = word
        
        response = bot.get_interview_questions(company, experience)
        formatted = bot.format_response(response)
        
        return {
            "type": "questions",
            "content": formatted
        }
    
    # Show categories
    elif "categories" in message or "topics" in message:
        categories = bot.get_categories()
        response = "Here are the available categories and their topics:\n\n"
        for category, topics in categories.items():
            response += f"{category}:\n"
            for topic in topics:
                response += f"  - {topic}\n"
        
        return {
            "type": "categories",
            "content": response
        }
    
    # Show companies
    elif "companies" in message:
        companies = bot.get_available_companies()
        response = "Here are the companies I have questions for:\n\n"
        response += "\n".join(f"- {company}" for company in companies)
        
        return {
            "type": "companies",
            "content": response
        }
    
    # Help message
    elif "help" in message:
        return {
            "type": "help",
            "content": (
                "Here's how you can interact with me:\n\n"
                "- Ask for questions: 'Show me TCS interview questions for 2 years experience'\n"
                "- View categories: 'What categories of questions do you have?'\n"
                "- List companies: 'Which companies do you have questions for?'\n"
                "- Get specific: 'Show me Selenium questions for Microsoft'\n"
                "- Filter by difficulty: 'Show me advanced questions for Amazon'\n\n"
                "You can also combine these: 'Show me advanced Selenium questions for TCS with 3 years experience'"
            )
        }
    
    # Default response
    return {
        "type": "text",
        "content": (
            "I'm not sure I understood that. You can:\n"
            "- Ask for company specific questions\n"
            "- View question categories\n"
            "- List available companies\n"
            "- Type 'help' for more details\n"
        )
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)