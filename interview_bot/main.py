from interview_bot import InterviewBot
import sys

def clear_screen():
    """Clear the console screen"""
    print("\033[H\033[J", end="")

def display_menu():
    print("\n=== Automation Testing Interview Question Bot ===")
    print("1. Search Questions")
    print("2. Browse by Company")
    print("3. Browse by Category")
    print("4. Show Statistics")
    print("5. Help")
    print("6. Exit")
    return input("\nSelect an option (1-6): ")

def get_valid_input(prompt, valid_options=None, is_number=False):
    """Get and validate user input"""
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue
        
        if is_number:
            try:
                float(user_input)
                return user_input
            except ValueError:
                print("Please enter a valid number.")
                continue
                
        if valid_options and user_input.lower() not in [opt.lower() for opt in valid_options]:
            print(f"Please enter one of: {', '.join(valid_options)}")
            continue
            
        return user_input

def search_questions(bot):
    """Search for interview questions with filters"""
    print("\n=== Search Interview Questions ===")
    
    # Get company
    companies = bot.get_available_companies()
    print("\nAvailable companies:")
    for i, company in enumerate(companies, 1):
        print(f"{i}. {company}")
    company = get_valid_input("\nEnter company name: ", companies)
    
    # Get experience
    years = get_valid_input("Enter years of experience: ", is_number=True)
    
    # Optional filters
    categories = list(bot.get_categories().keys())
    difficulty_levels = list(bot.get_difficulty_levels().keys())
    
    use_filters = get_valid_input("\nWould you like to apply filters? (yes/no): ", ["yes", "no"]).lower()
    
    category = None
    difficulty = None
    
    if use_filters == "yes":
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        use_category = get_valid_input("\nFilter by category? (yes/no): ", ["yes", "no"]).lower()
        if use_category == "yes":
            category = get_valid_input("Enter category: ", categories)
            
        print("\nDifficulty levels:")
        for i, level in enumerate(difficulty_levels, 1):
            print(f"{i}. {level}")
        use_difficulty = get_valid_input("\nFilter by difficulty? (yes/no): ", ["yes", "no"]).lower()
        if use_difficulty == "yes":
            difficulty = get_valid_input("Enter difficulty level: ", difficulty_levels)
    
    try:
        response = bot.get_interview_questions(company, years, category, difficulty)
        print(bot.format_response(response))
    except Exception as e:
        print(f"\nError: {str(e)}")

def browse_companies(bot):
    """Browse and list companies"""
    print("\n=== Browse Companies ===")
    companies = bot.get_available_companies()
    
    print("\nAvailable Companies:")
    for i, company in enumerate(companies, 1):
        print(f"{i}. {company}")
    
    print("\nTotal companies:", len(companies))

def browse_categories(bot):
    """Browse categories and their topics"""
    print("\n=== Browse Categories ===")
    categories = bot.get_categories()
    
    for category, topics in categories.items():
        print(f"\n{category}:")
        for topic in topics:
            print(f"  - {topic}")

def show_statistics(bot):
    """Show database statistics"""
    print("\n=== Interview Questions Statistics ===")
    
    companies = bot.get_available_companies()
    categories = bot.get_categories()
    difficulty_levels = bot.get_difficulty_levels()
    
    print(f"\nTotal Companies: {len(companies)}")
    print(f"Total Categories: {len(categories)}")
    print(f"Difficulty Levels: {', '.join(difficulty_levels.keys())}")
    
    print("\nCategories Overview:")
    for category in categories:
        print(f"- {category}")

def show_help():
    """Show help information"""
    print("\n=== Help ===")
    print("This bot helps you find relevant interview questions for automation testing roles.")
    print("\nFeatures:")
    print("1. Search Questions - Search with company name and experience level")
    print("2. Browse Companies - View all available companies")
    print("3. Browse Categories - Explore different question categories")
    print("4. Statistics - View database statistics")
    print("\nTips:")
    print("- Use filters to narrow down questions by category or difficulty")
    print("- Check multiple companies to prepare comprehensively")
    print("- Review questions from different experience levels")

def main():
    try:
        bot = InterviewBot()
        
        print("Welcome to the Automation Testing Interview Question Bot!")
        print("=" * 60)
        print("This bot contains interview questions from top Indian companies for automation testing roles")
        
        while True:
            try:
                choice = display_menu()
                
                if choice == "1":
                    search_questions(bot)
                elif choice == "2":
                    browse_companies(bot)
                elif choice == "3":
                    browse_categories(bot)
                elif choice == "4":
                    show_statistics(bot)
                elif choice == "5":
                    show_help()
                elif choice == "6":
                    break
                else:
                    print("\nInvalid option. Please try again.")
                
                input("\nPress Enter to continue...")
                clear_screen()
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                continue
                
    except Exception as e:
        print(f"\nError: An unexpected error occurred - {str(e)}")
        sys.exit(1)
        
    print("\nThank you for using the Interview Question Bot!")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()