import os
import sys
import streamlit as st
from datetime import datetime

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from interview_bot.interview_bot import InterviewBot
from interview_bot.chat_interface import ChatBot

def setup_page():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="Interview Preparation Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton > button {
            width: 100%;
            border-radius: 20px;
            height: 3em;
            font-size: 16px;
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .bot-message {
            background-color: #f0f2f6;
        }
        .user-message {
            background-color: #e6f3ff;
        }
        .message-content {
            margin-top: 0.5rem;
        }
        .category-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .markdown-text pre {
            padding: 1rem;
            background-color: #f8f9fa;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .company-tag {
            background-color: #e1e4e8;
            padding: 0.2rem 0.5rem;
            border-radius: 15px;
            font-size: 0.8em;
            margin-right: 0.5rem;
        }
        .difficulty-easy {
            color: #28a745;
        }
        .difficulty-medium {
            color: #ffc107;
        }
        .difficulty-hard {
            color: #dc3545;
        }
        .sidebar-content {
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_bot' not in st.session_state:
        st.session_state.chat_bot = ChatBot()
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None

def display_chat_message(role, message):
    """Display a chat message with appropriate styling"""
    message_class = "bot-message" if role == "bot" else "user-message"
    
    with st.container():
        st.markdown(f"""
            <div class="chat-message {message_class}">
                <div><strong>{'🤖 Bot' if role == 'bot' else '👤 You'}</strong></div>
                <div class="message-content">{message}</div>
            </div>
        """, unsafe_allow_html=True)

def display_code_question(question):
    """Display a coding question with formatting"""
    st.markdown(f"""
        <div class="category-card">
            <h3>{question['question']}</h3>
            <p><span class="difficulty-{question['difficulty'].lower()}">{question['difficulty']}</span> | {question['category']}</p>
            <h4>Template:</h4>
            <pre><code>{question['code_template']}</code></pre>
            <h4>Hints:</h4>
            <ul>{''.join([f'<li>{hint}</li>' for hint in question['hints']])}</ul>
            <h4>Test Cases:</h4>
            <ul>{''.join([f'<li>{test}</li>' for test in question['test_cases']])}</ul>
        </div>
    """, unsafe_allow_html=True)

def save_chat_history():
    """Save the chat history to a file"""
    if not os.path.exists('chat_history'):
        os.makedirs('chat_history')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'chat_history/conversation_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(st.session_state.conversation, f, indent=2)
    
    return filename

def display_sidebar():
    """Display and handle sidebar content"""
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-content">
                <h2>Interview Preparation Assistant</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Quick Actions")
        
        if st.button("📋 View Categories"):
            response = st.session_state.chat_bot.process_message("categories")
            st.session_state.conversation.append({"role": "user", "message": "Show categories"})
            st.session_state.conversation.append({"role": "bot", "message": response})

        if st.button("💼 List Companies"):
            response = st.session_state.chat_bot.process_message("companies")
            st.session_state.conversation.append({"role": "user", "message": "Show companies"})
            st.session_state.conversation.append({"role": "bot", "message": response})

        if st.button("💻 Coding Questions"):
            response = st.session_state.chat_bot.process_message("coding categories")
            st.session_state.conversation.append({"role": "user", "message": "Show coding categories"})
            st.session_state.conversation.append({"role": "bot", "message": response})

        st.markdown("### Settings")
        if st.button("💾 Save Chat"):
            filename = save_chat_history()
            st.success(f"Chat saved to {filename}")

        if st.button("🗑️ Clear Chat"):
            st.session_state.conversation = []
            st.session_state.current_question = None
            st.success("Chat cleared!")

        st.markdown("### Help")
        with st.expander("ℹ️ Usage Guide"):
            st.markdown("""
                **Example commands:**
                - "Show me TCS interview questions"
                - "Give me coding questions"
                - "What are behavioral questions?"
                - "Show system design questions"
                - "Show me HR interview tips"
            """)

def main():
    setup_page()
    initialize_session_state()
    
    # Display sidebar
    display_sidebar()
    
    # Main chat interface
    st.markdown("## 💬 Chat")
    
    # Display conversation history
    for message in st.session_state.conversation:
        display_chat_message(message["role"], message["message"])
    
    # User input
    user_input = st.text_input("Type your message here...", key="user_input")
    
    # Handle user input
    if user_input:
        st.session_state.conversation.append({"role": "user", "message": user_input})
        
        # Get bot response
        response = st.session_state.chat_bot.process_message(user_input)
        st.session_state.conversation.append({"role": "bot", "message": response})
        
        # Clear input
        st.text_input("Type your message here...", value="", key="user_input_clear")
        
        # Rerun to update the display
        st.experimental_rerun()

if __name__ == "__main__":
    main()