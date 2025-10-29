from interview_bot.interview_bot import InterviewBot

bot = InterviewBot()

# Test retrieval of new Playwright questions
response = bot.get_interview_questions("Popular Interview Questions", 2, category="Playwright")
print(bot.format_response(response))