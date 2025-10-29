import os
import sys

def print_paths():
    print("Current working directory:", os.getcwd())
    print("\nPython path:")
    for p in sys.path:
        print(f"  {p}")

def test_imports():
    print("\nTesting imports...")
    
    try:
        import interview_bot
        print("✓ Successfully imported interview_bot package")
        
        from interview_bot import InterviewBot
        print("✓ Successfully imported InterviewBot class")
        
        from interview_bot import ChatBot
        print("✓ Successfully imported ChatBot class")
        
        from interview_bot import QuestionAggregator
        print("✓ Successfully imported QuestionAggregator class")
        
        bot = InterviewBot()
        print("✓ Successfully created InterviewBot instance")
        
        chat = ChatBot()
        print("✓ Successfully created ChatBot instance")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()

if __name__ == "__main__":
    # Add the repository root to Python path
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.append(repo_root)
    
    print("=== Python Environment Information ===")
    print_paths()
    print("\n=== Import Tests ===")
    test_imports()