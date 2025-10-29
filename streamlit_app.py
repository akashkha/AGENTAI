import streamlit as st
from interview_bot.bot import InterviewBot
import os

# Initialize session state
def init_session_state():
    default_values = {
        'bot': InterviewBot(),
        'messages': [],
        'bot_mode': 'Chat',
        'chat_input': ""
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

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

# Initialize bot and cache data
if 'bot' not in st.session_state:
    try:
        st.session_state.bot = InterviewBot()
    except Exception as e:
        st.error(f"Failed to initialize bot. Please try refreshing the page.")
        st.stop()

# Initialize session data
if 'companies' not in st.session_state:
    try:
        companies = st.session_state.bot.get_available_companies()
        if not companies:
            st.error("Failed to load companies.")
            st.stop()
        st.session_state.companies = companies
    except Exception as e:
        st.error(f"Error loading companies: {str(e)}")
        st.stop()
    
# Get all unique categories including subcategories
if 'categories' not in st.session_state:
    try:
        categories = st.session_state.bot.get_categories()
        if not categories:
            st.error("Failed to load categories. Please check debug information.")
            st.stop()
        all_categories = set()
        for main_category, subcategories in categories.items():
            all_categories.add(main_category)
            all_categories.update(subcategories)
        st.session_state.categories = ["All"] + sorted(list(all_categories))
    except Exception as e:
        st.error(f"Error loading categories: {str(e)}")
        st.stop()
    
if 'difficulty_levels' not in st.session_state:
    try:
        difficulty_levels = st.session_state.bot.get_difficulty_levels()
        if not difficulty_levels:
            st.error("Failed to load difficulty levels. Please check debug information.")
            st.stop()
        st.session_state.difficulty_levels = ["All"] + difficulty_levels
    except Exception as e:
        st.error(f"Error loading difficulty levels: {str(e)}")
        st.stop()

# Quick Access Section
st.markdown("### 🚀 Quick Access")

# Company search and selection
search_or_select = st.radio(
    "How would you like to find questions?",
    ["Select from list", "Search any company"],
    horizontal=True,
    help="Choose whether to select from existing companies or search across all questions"
)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if search_or_select == "Select from list":
        # Enhanced company selection
        def format_company(company):
            total_questions = 0
            # Count questions for all experience levels
            for exp in ["0-2", "2-5"]:
                questions = st.session_state.bot.get_interview_questions(company, exp)
                total_questions += len(questions) if questions else 0
            return f"{company} • {total_questions} Q's"

        selected_company = st.selectbox(
            "Select Company",
            st.session_state.companies,
            format_func=format_company,
            help="Select a company from the list"
        )
    else:
        # Free text search for companies
        search_company = st.text_input(
            "Enter company name",
            help="Type any company name to search across all questions"
        )
        selected_company = search_company if search_company else ""

with col2:
    experience = st.slider(
        "Years of Experience",
        0, 10, 2,
        help="Select your years of experience"
    )

with col3:
    selected_category = st.selectbox(
        "Select Category",
        st.session_state.categories,
        help="Filter questions by category"
    )

with col4:
    selected_difficulty = st.selectbox(
        "Select Difficulty",
        st.session_state.difficulty_levels,
        help="Filter questions by difficulty level"
    )

# Search box
search_query = st.text_input(
    "🔍 Search for specific questions",
    help="Enter keywords to search across all questions"
)

if search_query:
    search_results = st.session_state.bot.search_questions(search_query)
    if search_results:
        st.markdown("### Search Results")
        for result in search_results:
            with st.expander(f"Question from {result['company']} ({result['experience']} years)"):
                st.write(f"**Category:** {result.get('category', 'General')}")
                st.write(f"**Difficulty:** {result.get('difficulty', 'Medium')}")
                st.write(f"**Q:** {result['question']}")
                if result.get('answer'):
                    st.write(f"**A:** {result['answer']}")

# Get Questions button
if st.button("Get Questions", type="primary"):
    category = None if selected_category == "All" else selected_category
    difficulty = None if selected_difficulty == "All" else selected_difficulty
    response = st.session_state.bot.get_interview_questions(
        selected_company,
        experience,
        category,
        difficulty
    )
    
    # Show results in an organized way
    st.markdown("### Results")
    formatted_response = st.session_state.bot.format_response(response)
    
    # Split the response into questions
    questions = formatted_response.split("-" * 80)
    
    # Show header
    st.markdown(questions[0])
    
    # Show each question in an expander
    for question in questions[1:-1]:  # Skip header and empty last element
        if question.strip():
            # Extract the question title from the first line
            title = question.strip().split('\n')[0]
            with st.expander(title):
                st.markdown(question)

st.divider()
st.markdown("### 💬 Chat Interface")
st.markdown("Ask me anything about interview questions, or type 'help' for guidance.")

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a form for better input handling
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...")
    col1, col2 = st.columns([1, 5])
    with col1:
        submit_button = st.form_submit_button("Send")
    with col2:
        clear_chat = st.form_submit_button("Clear Chat")
    
    if submit_button and user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        bot_response = process_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    elif clear_chat:
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)