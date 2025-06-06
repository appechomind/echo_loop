# Simulates typing into ChatGPT using pyautogui

import keyboard
import time
import random
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='chatgpt_typer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def simulate_human_typing(text, min_delay=0.1, max_delay=0.3):
    """
    Simulates human-like typing with random delays between keystrokes.
    """
    for char in text:
        # Add random delay between keystrokes
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
        # Type the character
        keyboard.write(char)
        
        # Occasionally add a longer pause (like a human thinking)
        if random.random() < 0.05:  # 5% chance
            time.sleep(random.uniform(0.5, 1.5))

def type_response():
    """
    Reads the response from ai_2_out.txt and types it into the active window.
    """
    try:
        # 1. Read response
        with open("ai_2_out.txt", "r", encoding="utf-8") as f:
            response = f.read().strip()
        
        if not response:
            logging.warning("No response found in ai_2_out.txt")
            return False, "No response to type"
        
        # 2. Simulate typing
        logging.info(f"Starting to type response at {datetime.now().isoformat()}")
        logging.info(f"Response length: {len(response)} characters")
        
        # Add a small delay before starting to type
        time.sleep(1)
        
        # Type the response
        simulate_human_typing(response)
        
        # 3. Handle completion
        logging.info("Finished typing response")
        return True, "Successfully typed response"
        
    except Exception as e:
        error_msg = f"Error in type_response: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

def type_with_retry(max_retries=3):
    """
    Attempts to type the response with retries on failure.
    """
    for attempt in range(max_retries):
        success, message = type_response()
        if success:
            return True, message
        
        logging.warning(f"Attempt {attempt + 1} failed: {message}")
        time.sleep(2)  # Wait before retrying
    
    return False, f"Failed after {max_retries} attempts"

if __name__ == "__main__":
    print("Starting ChatGPT Typer test...")
    print("Please focus on the window where you want the text to be typed.")
    print("Press Enter to start typing (after 3 seconds)...")
    time.sleep(3)
    
    success, message = type_with_retry()
    print(f"Test {'succeeded' if success else 'failed'}: {message}")
