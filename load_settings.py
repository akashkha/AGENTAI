import os
from dotenv import load_dotenv
import json

def load_settings():
    # Load environment variables from .env file
    load_dotenv()
    
    # Read the template settings file
    with open('.github/agents/settings.json', 'r') as f:
        settings = json.load(f)
    
    # Update GitHub settings
    if 'github' in settings['mcpServers']:
        settings['mcpServers']['github']['env']['GITHUB_PERSONAL_ACCESS_TOKEN'] = os.getenv('GITHUB_TOKEN')
        settings['mcpServers']['github']['env']['GITHUB_HOST'] = os.getenv('GITHUB_HOST')
    
    # Update MySQL settings
    if 'mysql' in settings['mcpServers']:
        settings['mcpServers']['mysql']['env']['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
        settings['mcpServers']['mysql']['env']['MYSQL_PORT'] = os.getenv('MYSQL_PORT')
        settings['mcpServers']['mysql']['env']['MYSQL_USER'] = os.getenv('MYSQL_USER')
        settings['mcpServers']['mysql']['env']['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
        settings['mcpServers']['mysql']['env']['MYSQL_DATABASE'] = os.getenv('MYSQL_DATABASE')
    
    return settings

if __name__ == '__main__':
    try:
        settings = load_settings()
        print("Settings loaded successfully!")
    except Exception as e:
        print(f"Error loading settings: {str(e)}")