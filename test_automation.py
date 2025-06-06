import os
import time
import logging
from datetime import datetime
from browser_controller import BrowserController
from chatgpt_typer import type_with_retry
from screen_reader import capture_screen
from file_writer import write_changes

# Set up logging
logging.basicConfig(
    filename='automation_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_automation_flow():
    """
    Test the complete automation flow:
    1. Initialize browser
    2. Send message to ChatGPT
    3. Wait for response
    4. Capture screen
    5. Type response
    6. Write changes
    """
    logging.info("Starting automation test")
    
    # Create test input
    test_prompt = """
    Create a simple Python script that:
    1. Takes a number as input
    2. Calculates its factorial
    3. Prints the result
    """
    
    with open("ai_1_out.txt", "w", encoding="utf-8") as f:
        f.write(test_prompt)
    
    # Initialize browser controller
    controller = BrowserController()
    
    try:
        # 1. Initialize browser
        success, message = controller.initialize()
        if not success:
            logging.error(f"Failed to initialize browser: {message}")
            return False
        
        # Wait for user to log in
        print("Please log in to ChatGPT. Press Enter when ready...")
        input()
        
        # 2. Send message
        success, message = controller.send_message(test_prompt)
        if not success:
            logging.error(f"Failed to send message: {message}")
            return False
        
        # 3. Wait for response
        success, response = controller.wait_for_response()
        if not success:
            logging.error(f"Failed to get response: {response}")
            return False
        
        # Save response to ai_2_out.txt
        with open("ai_2_out.txt", "w", encoding="utf-8") as f:
            f.write(response)
        
        # 4. Capture screen
        screen_result = capture_screen()
        if not screen_result["success"]:
            logging.error(f"Failed to capture screen: {screen_result['error']}")
            return False
        
        # 5. Type response
        success, message = type_with_retry()
        if not success:
            logging.error(f"Failed to type response: {message}")
            return False
        
        # 6. Write changes
        success, message = write_changes()
        if not success:
            logging.error(f"Failed to write changes: {message}")
            return False
        
        logging.info("Automation test completed successfully")
        return True
        
    except Exception as e:
        logging.error(f"Unexpected error in automation test: {str(e)}")
        return False
        
    finally:
        controller.close()

if __name__ == "__main__":
    print("Starting automation system test...")
    success = test_automation_flow()
    print(f"Test {'succeeded' if success else 'failed'}")
    print("Check automation_test.log for details") 