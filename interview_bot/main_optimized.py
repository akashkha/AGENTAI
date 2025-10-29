from interview_bot import InterviewBot
import os

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n=== Interview Question Bot Menu ===")
    print("1. Quick Search by Company")
    print("2. Browse Companies")
    print("3. View Categories")
    print("4. Browse Question Sources")
    print("5. Popular Interview Questions")
    print("6. Coding Questions")
    print("7. Exit")
    return input("Select an option (1-7): ")

def main():
    # Initialize bot once at startup
    bot = InterviewBot()
    
    print("Welcome to the Automation Testing Interview Question Bot!")
    print("=" * 60)
    
    while True:
        try:
            choice = display_menu()
            
            if choice == "1":
                # Show available companies for reference
                companies = bot.get_available_companies()
                print("\nAvailable Companies by Domain:")
                
                # Group companies by domain
                domain_companies = {}
                for company in companies:
                    domain = bot.get_company_domain(company)
                    if domain not in domain_companies:
                        domain_companies[domain] = []
                    domain_companies[domain].append(company)
                
                # Print companies by domain
                for domain, comp_list in domain_companies.items():
                    print(f"\n{domain.upper()}:")
                    print("  " + ", ".join(comp_list))
                
                print("\nNote: You can enter ANY company name. The system will provide relevant questions based on the company's domain.")
                
                while True:
                    company = input("\nEnter company name (or 'back' to return to menu): ").strip()
                    if company.lower() == 'back':
                        break
                    if not company:
                        print("Company name cannot be empty!")
                        print("Type a company name to get interview questions specific to that company or its domain.")
                        continue
                    
                    try:
                        years = input("Enter years of experience (e.g., 2.5): ").strip()
                        if not years:
                            print("Years of experience cannot be empty!")
                            continue
                        
                        # Validate years format
                        float(years)  # This will raise ValueError if not a valid number
                        
                        # Get optional filters
                        print("\nOptional Filters (press Enter to skip):")
                        categories = bot.get_categories()
                        print("\nAvailable Categories:")
                        for category in categories.keys():
                            print(f"- {category}")
                        category = input("Enter category name: ").strip()
                        
                        difficulty_levels = bot.get_difficulty_levels()
                        print("\nAvailable Difficulty Levels:")
                        for level, desc in difficulty_levels.items():
                            print(f"- {level}: {desc}")
                        difficulty = input("Enter difficulty level: ").strip()
                        
                        # If category or difficulty is empty, pass None
                        category = category if category else None
                        difficulty = difficulty if difficulty else None
                        
                        response = bot.get_interview_questions(company, years, category, difficulty)
                        print(bot.format_response(response))
                        
                        another = input("\nWould you like to search for another company? (yes/no): ").strip().lower()
                        if another != 'yes':
                            break
                            
                    except ValueError as e:
                        print(f"\nError: Please enter a valid number for years of experience")
                    except Exception as e:
                        print(f"\nUnexpected error: {str(e)}")

            elif choice == "2":
                companies = bot.get_available_companies()
                print("\nAvailable Companies:")
                print("=" * 60)
                for i, company in enumerate(companies, 1):
                    # Get total questions for each experience range
                    total_questions = sum(len(bot.questions_db["companies"][company].get(exp, [])) 
                                       for exp in ["0-2", "2-5"])
                    print(f"{i}. {company} ({total_questions} questions available)")

            elif choice == "3":
                categories = bot.get_categories()
                print("\nAvailable Categories and Topics:")
                print("=" * 60)
                for category, topics in categories.items():
                    print(f"\n{category}:")
                    for topic in topics:
                        print(f"  - {topic}")
                    # Count questions in this category
                    category_count = sum(1 for company in bot.questions_db["companies"].values()
                                      for exp_range in company.values()
                                      for question in exp_range
                                      if question["category"] == category)
                    print(f"  Total questions in this category: {category_count}")

            elif choice == "4":
                sources = bot.get_sources()
                print("\nAvailable Question Sources:")
                print("=" * 60)
                for source, description in sources.items():
                    print(f"\n{source}:")
                    print(f"Description: {description}")
                    # Count questions from this source
                    source_count = sum(1 for company in bot.questions_db["companies"].values()
                                    for exp_range in company.values()
                                    for question in exp_range
                                    if question.get("source") == source)
                    if source_count > 0:
                        print(f"Questions from this source: {source_count}")
                    
            elif choice == "5":
                print("\nPopular Interview Questions:")
                print("=" * 60)
                # Show questions for both experience ranges
                for exp in ["0-2", "2-5"]:
                    print(f"\nExperience Range: {exp} years")
                    print("-" * 40)
                    response = bot.get_interview_questions("Popular Interview Questions", exp)
                    print(bot.format_response(response))
                
            elif choice == "6":
                print("\nCoding Questions Categories:")
                print("=" * 60)
                print("1. Automation Coding Problems")
                print("2. Data Structure & Algorithms")
                print("3. System Design")
                print("4. SQL Problems")
                print("5. API Testing Code Challenges")
                print("6. Back to Main Menu")
                
                while True:
                    coding_choice = input("\nSelect a category (1-6): ").strip()
                    if coding_choice == "6":
                        break
                        
                    try:
                        years = input("Enter years of experience (e.g., 2.5): ").strip()
                        if not years:
                            print("Years of experience cannot be empty!")
                            continue
                            
                        # Validate years format
                        float(years)
                        
                        # Get difficulty level
                        print("\nDifficulty Levels:")
                        print("1. Easy")
                        print("2. Medium")
                        print("3. Hard")
                        print("4. All Levels")
                        
                        difficulty = input("\nSelect difficulty (1-4): ").strip()
                        
                        category_map = {
                            "1": "Automation",
                            "2": "DSA",
                            "3": "System Design",
                            "4": "SQL",
                            "5": "API Testing"
                        }
                        
                        difficulty_map = {
                            "1": "Easy",
                            "2": "Medium",
                            "3": "Hard",
                            "4": None
                        }
                        
                        if coding_choice in category_map:
                            response = bot.get_coding_questions(
                                category_map[coding_choice],
                                years,
                                difficulty_map.get(difficulty)
                            )
                            print(bot.format_response(response))
                        
                    except ValueError:
                        print("\nPlease enter a valid number for years of experience")
                    except Exception as e:
                        print(f"\nUnexpected error: {str(e)}")
                        
                    another = input("\nWould you like to see more coding questions? (yes/no): ").strip().lower()
                    if another != 'yes':
                        break
                        
            elif choice == "7":
                break
            
            else:
                print("\nInvalid option! Please select a number between 1-6.")
            
            input("\nPress Enter to continue...")
            clear_screen()
            
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            input("\nPress Enter to continue...")
    
    print("\nThank you for using the Interview Question Bot!")

if __name__ == "__main__":
    main()