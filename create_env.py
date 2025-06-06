#!/usr/bin/env python3
"""
Script to create the .env file for EchoLoop automation system
"""

def create_env_file():
    env_content = """# API Keys
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
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Contents:")
        print(env_content)
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

if __name__ == "__main__":
    create_env_file() 