import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(__file__))
from interview_bot.interview_bot import InterviewBot

# Initialize session state
def init_session_state():
    if 'bot' not in st.session_state:
        st.session_state.bot = InterviewBot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'bot_mode' not in st.session_state:
        st.session_state.bot_mode = 'Chat'
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

# Initialize everything at startup
init_session_state()

def process_message(message):
    """Process user message and return bot response"""
    message = message.lower().strip()
    bot = st.session_state.bot
    
    # Initial greeting
    if any(greeting in message for greeting in ['hi', 'hello', 'hey']):
        return (
            "Hello! I'm your Interview Preparation Assistant. I can help you with:\n"
            "1. Finding interview questions for specific companies\n"
            "2. Questions by experience level\n"
            "3. Questions by category (like Selenium, API Testing, etc.)\n"
            "4. Questions by difficulty level\n\n"
            "What would you like to know about?"
        )
    
    # Company specific questions
    elif "questions" in message and any(company.lower() in message for company in bot.get_available_companies()):
        company = next(c for c in bot.get_available_companies() if c.lower() in message.lower())
        
        # Try to extract experience from message
        experience = "2"  # default
        for word in message.split():
            if word.replace('.', '').isdigit():
                experience = word
        
        response = bot.get_interview_questions(company, experience)
        return bot.format_response(response)
    
    # Show categories
    elif "categories" in message or "topics" in message:
        categories = bot.get_categories()
        response = "Here are the available categories and their topics:\n\n"
        for category, topics in categories.items():
            response += f"{category}:\n"
            for topic in topics:
                response += f"  - {topic}\n"
        return response
    
    # Show companies
    elif "companies" in message:
        companies = bot.get_available_companies()
        response = "Here are the companies I have questions for:\n\n"
        response += "\n".join(f"- {company}" for company in companies)
        return response
    
    # Help message
    elif "help" in message:
        return (
            "Here's how you can interact with me:\n\n"
            "- Ask for questions: 'Show me TCS interview questions for 2 years experience'\n"
            "- View categories: 'What categories of questions do you have?'\n"
            "- List companies: 'Which companies do you have questions for?'\n"
            "- Get specific: 'Show me Selenium questions for Microsoft'\n"
            "- Filter by difficulty: 'Show me advanced questions for Amazon'\n\n"
            "You can also combine these: 'Show me advanced Selenium questions for TCS with 3 years experience'"
        )
    
    # Default response
    return (
        "I'm not sure I understood that. You can:\n"
        "- Ask for company specific questions\n"
        "- View question categories\n"
        "- List available companies\n"
        "- Type 'help' for more details\n"
    )

# Set page config
st.set_page_config(
    page_title="Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.user-message {
    background-color: #075E54;
    color: white;
    padding: 15px;
    border-radius: 15px;
    margin: 5px 0;
}
.bot-message {
    background-color: #DCF8C6;
    color: black;
    padding: 15px;
    border-radius: 15px;
    margin: 5px 0;
}
.stTextInput>div>div>input {
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# App title
st.title("🤖 Interview Preparation Assistant")
st.markdown("Ask me about interview questions for different companies and roles!")

# Initialize session state for bot mode
if 'bot_mode' not in st.session_state:
    st.session_state.bot_mode = 'chat'

# Sidebar for mode selection and filters
with st.sidebar:
    st.title("Options")
    st.session_state.bot_mode = st.radio("Select Mode", ['Chat', 'Browse Questions', 'View Categories'])
    
    if st.session_state.bot_mode == 'Browse Questions':
        st.subheader("Filters")
        companies = st.session_state.bot.get_available_companies()
        selected_company = st.selectbox("Select Company", companies)
        experience = st.slider("Years of Experience", 0, 10, 2)
        categories = list(st.session_state.bot.get_categories().keys())
        selected_category = st.selectbox("Select Category", ["All"] + categories)
        
        if st.button("Get Questions"):
            category = selected_category if selected_category != "All" else None
            response = st.session_state.bot.get_interview_questions(selected_company, experience, category)
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.bot.format_response(response)})

# Main chat interface
if st.session_state.bot_mode == 'Chat':
    # Chat input
    user_input = st.text_input("Type your message here...", key="user_input")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        bot_response = process_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Clear input using the proper Streamlit way
        st.session_state["user_input"] = ""
        st.experimental_rerun()

# Display categories
elif st.session_state.bot_mode == 'View Categories':
    categories = st.session_state.bot.get_categories()
    for category, topics in categories.items():
        with st.expander(f"{category} Topics"):
            for topic in topics:
                st.write(f"- {topic}")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()