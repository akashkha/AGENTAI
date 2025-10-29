import os
import zipfile
from datetime import datetime

def create_zip():
    # Create timestamp for zip file name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name = f'interview_bot_package_{timestamp}.zip'
    
    # Files to include
    files_to_zip = [
        'interview_bot/chat_interface.py',
        'interview_bot/interview_bot.py',
        'interview_bot/questions_db.json',
        'interview_bot/string_matcher.py',
        'requirements.txt',
        'README.md',
        'start_interview_bot.bat'
    ]
    
    # Create zip file
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
    
    print(f"\nPackage created: {zip_name}")
    print("Share this file with your friends!")

if __name__ == "__main__":
    create_zip()