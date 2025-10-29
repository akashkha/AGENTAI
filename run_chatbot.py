import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interview_bot.chat_interface import main

if __name__ == "__main__":
    main()