import streamlit as st
from interview_bot.bot import InterviewBot
import os

# Initialize bot
if 'bot' not in st.session_state:
    st.session_state.bot = InterviewBot()
    print("Bot initialized successfully")

# Set page config
st.set_page_config(
    page_title="Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    padding: 1rem;
    font-size: 1.1rem;
}
.question-box {
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title("🤖 Interview Question Assistant")
st.write("Get relevant interview questions for any company!")

# Main Interface
st.header("🔍 Search Questions")

col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input(
        "Enter Company Name",
        placeholder="e.g., Amdocs, TCS, Microsoft",
        help="Type any company name to get relevant questions"
    )
    
    years_exp = st.slider(
        "Years of Experience",
        0, 10, 2,
        help="Select your years of experience"
    )

with col2:
    categories = ["All", "Selenium", "API Testing", "Framework Design", "TestNG"]
    category = st.selectbox(
        "Select Category",
        categories,
        help="Choose a specific category of questions"
    )
    
    difficulties = ["All", "Basic", "Medium", "Advanced"]
    difficulty = st.selectbox(
        "Select Difficulty",
        difficulties,
        help="Choose the difficulty level of questions"
    )

# Search button
if st.button("🔍 Get Questions", type="primary", key="search"):
    if company_name:
        with st.spinner(f"Searching questions for {company_name}..."):
            try:
                # Get questions
                response = st.session_state.bot.get_interview_questions(
                    company_name,
                    years_exp,
                    None if category == "All" else category,
                    None if difficulty == "All" else difficulty
                )
                
                if response.get("questions"):
                    st.success(f"Found {len(response['questions'])} questions!")
                    
                    # Display questions in a clean format
                    for i, q in enumerate(response["questions"], 1):
                        with st.expander(f"Question #{i}: {q.get('question', '')[:100]}..."):
                            st.markdown(f"**Source:** {q.get('source', 'Generated')} :link:")
                            st.markdown(f"**Category:** {q.get('category', 'General')}")
                            st.markdown(f"**Difficulty:** {q.get('difficulty', 'Medium')}")
                            st.markdown(f"**Question:**\n{q.get('question')}")
                            if q.get('answer'):
                                st.markdown(f"**Answer:**\n{q.get('answer')}")
                            if q.get('followup'):
                                st.markdown(f"**Follow-up:**\n{q.get('followup')}")
                            if q.get('followup_answer'):
                                st.markdown(f"**Follow-up Answer:**\n{q.get('followup_answer')}")
                else:
                    st.warning("No questions found. Trying without filters...")
                    # Retry without filters
                    response = st.session_state.bot.get_interview_questions(
                        company_name,
                        years_exp
                    )
                    if response.get("questions"):
                        st.success(f"Found {len(response['questions'])} general questions!")
                        for i, q in enumerate(response["questions"], 1):
                            with st.expander(f"Question #{i}: {q.get('question', '')[:100]}..."):
                                st.markdown(f"**Category:** {q.get('category', 'General')}")
                                st.markdown(f"**Question:**\n{q.get('question')}")
                                if q.get('answer'):
                                    st.markdown(f"**Answer:**\n{q.get('answer')}")
                    else:
                        st.error("No questions found. Please try a different company or category.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please try again with different search criteria.")
    else:
        st.warning("Please enter a company name!")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** If you don't get results, try:")
st.markdown("1. Using different categories")
st.markdown("2. Selecting 'All' for category and difficulty")
st.markdown("3. Checking company name spelling")