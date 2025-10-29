import os
import sys
import streamlit as st

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from interview_bot import InterviewBot, ChatBot
except ImportError as e:
    st.error(f"Failed to import interview_bot modules: {str(e)}")
    st.stop()

def init_session_state():
    """Initialize session state"""
    if 'chat_bot' not in st.session_state:
        try:
            st.session_state.chat_bot = ChatBot()
        except Exception as e:
            st.error(f"Failed to initialize ChatBot: {str(e)}")
            st.stop()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    st.set_page_config(
        page_title="Interview Bot",
        page_icon="🤖",
        layout="wide"
    )
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    try:
        init_session_state()
    except Exception as e:
        st.error(f"Failed to initialize session state: {str(e)}")
        st.stop()

    st.title("Interview Preparation Assistant")

    # Sidebar with improved response handling
    with st.sidebar:
        st.header("Options")
        
        # Quick Actions
        st.subheader("Quick Actions")
        if st.button("📚 View Categories"):
            response = st.session_state.chat_bot.process_message("categories")
            st.session_state.messages.append({"role": "user", "content": "Show me the categories"})
            st.session_state.messages.append({"role": "bot", "content": response})
        
        if st.button("🏢 List Companies"):
            response = st.session_state.chat_bot.process_message("companies")
            st.session_state.messages.append({"role": "user", "content": "Show me the companies"})
            st.session_state.messages.append({"role": "bot", "content": response})
            
        if st.button("💻 Coding Questions"):
            response = st.session_state.chat_bot.process_message("coding categories")
            st.session_state.messages.append({"role": "user", "content": "Show me coding questions"})
            st.session_state.messages.append({"role": "bot", "content": response})
            
        # Help section
        st.markdown("---")
        with st.expander("ℹ️ Help"):
            st.markdown("""
            **Example questions:**
            - Show me TCS interview questions
            - What are the technical questions?
            - Give me coding practice questions
            - Show system design questions
            """)

    # Main chat interface
    st.markdown("""
        <style>
        .user-message { 
            background-color: #e6f3ff; 
            padding: 15px; 
            border-radius: 15px; 
            margin: 8px 0; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .bot-message { 
            background-color: #f0f2f6; 
            padding: 15px; 
            border-radius: 15px; 
            margin: 8px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTextInput > div > div > input {
            background-color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-message'>You: {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>Bot: {msg['content']}</div>", unsafe_allow_html=True)
    
    # Chat input and processing
    with st.container():
        user_input = st.text_input("Ask a question:", key="user_input", disabled=st.session_state.processing)
        if user_input and user_input != st.session_state.get('last_input', '') and not st.session_state.processing:
            try:
                # Update last input to prevent reprocessing
                st.session_state.last_input = user_input
                
                # Add user message to history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get bot response
                response = st.session_state.chat_bot.process_message(user_input)
                
                # Add bot response to history
                st.session_state.messages.append({"role": "bot", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Add a clear button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()