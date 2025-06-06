#!/usr/bin/env python3
"""
Fix the .env file with proper formatting
"""

def create_env():
    content = """# API Keys
GEMINI_API_KEY=AIzaSyB1LBl9v8HQ2fH8dAnrPQHN_Hx8dReWJSE

# Browser Settings
BROWSER_HEADLESS=False
BROWSER_TIMEOUT=30

# Automation Settings
MAX_RETRIES=3
RETRY_DELAY=5
ITERATION_DELAY=1

# Git Settings
GIT_REPO_URL=https://github.com/appechomind/echo_loop_control.git
GIT_BRANCH=main

# Logging Settings
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ .env file created successfully!")
    print("\n📋 Contents:")
    print(content)

if __name__ == "__main__":
    create_env() 