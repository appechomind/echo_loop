import os
import sys
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    filename='setup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        logging.error("Python 3.8 or higher is required")
        return False
    return True

def install_requirements():
    """Install required packages."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logging.info("Successfully installed requirements")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install requirements: {str(e)}")
        return False

def check_tesseract():
    """Check if Tesseract OCR is installed."""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        logging.info("Tesseract OCR is properly installed")
        return True
    except Exception as e:
        logging.error(f"Tesseract OCR is not properly installed: {str(e)}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'templates', 'static']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    logging.info("Created necessary directories")

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_path = Path('.env')
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write("""# API Keys
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key

# Browser Settings
BROWSER_HEADLESS=False
BROWSER_TIMEOUT=30

# Automation Settings
MAX_RETRIES=3
RETRY_DELAY=5
ITERATION_DELAY=1

# Git Settings
GIT_REPO_URL=your_git_repo_url
GIT_BRANCH=main

# Logging Settings
LOG_LEVEL=INFO
""")
        logging.info("Created .env file template")

def check_git():
    """Check if Git is installed and configured."""
    try:
        import git
        repo = git.Repo('.')
        logging.info("Git repository is properly initialized")
        return True
    except git.InvalidGitRepositoryError:
        try:
            repo = git.Repo.init('.')
            logging.info("Initialized new Git repository")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize Git repository: {str(e)}")
            return False
    except Exception as e:
        logging.error(f"Git check failed: {str(e)}")
        return False

def main():
    """Main setup function."""
    print("Starting setup...")
    
    # Check Python version
    if not check_python_version():
        print("Error: Python 3.8 or higher is required")
        return False
    
    # Install requirements
    print("Installing requirements...")
    if not install_requirements():
        print("Error: Failed to install requirements")
        return False
    
    # Check Tesseract
    print("Checking Tesseract OCR...")
    if not check_tesseract():
        print("Warning: Tesseract OCR is not properly installed")
        print("Please install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Create directories
    print("Creating directories...")
    create_directories()
    
    # Create .env file
    print("Creating .env file...")
    create_env_file()
    
    # Check Git
    print("Checking Git configuration...")
    if not check_git():
        print("Warning: Git is not properly configured")
        print("Please configure Git with your repository URL")
    
    print("\nSetup completed!")
    print("\nNext steps:")
    print("1. Edit the .env file with your API keys and settings")
    print("2. Install Tesseract OCR if not already installed")
    print("3. Configure Git repository URL")
    print("4. Run the automation system using: python echo_loop.py")
    
    return True

if __name__ == "__main__":
    main() 