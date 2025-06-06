from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from datetime import datetime
import time

# Set up logging
logging.basicConfig(
    filename='browser_controller.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BrowserController:
    def __init__(self):
        self.driver = None
        self.wait = None
    
    def initialize(self):
        """
        Initialize the browser and navigate to ChatGPT.
        """
        try:
            # Initialize Chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            # Navigate to ChatGPT
            self.driver.get('https://chat.openai.com')
            logging.info("Browser initialized and navigated to ChatGPT")
            return True, "Browser initialized successfully"
            
        except Exception as e:
            error_msg = f"Failed to initialize browser: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def wait_for_input_box(self):
        """
        Wait for the ChatGPT input box to be available.
        """
        try:
            input_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-id='root']"))
            )
            return True, input_box
        except TimeoutException:
            error_msg = "Timeout waiting for input box"
            logging.error(error_msg)
            return False, error_msg
    
    def send_message(self, message):
        """
        Send a message to ChatGPT.
        """
        try:
            # Wait for and find the input box
            success, result = self.wait_for_input_box()
            if not success:
                return False, result
            
            input_box = result
            
            # Type the message
            input_box.send_keys(message)
            logging.info(f"Typed message: {message[:50]}...")
            
            # Find and click the send button
            send_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='send-button']"))
            )
            send_button.click()
            logging.info("Message sent")
            
            return True, "Message sent successfully"
            
        except Exception as e:
            error_msg = f"Error sending message: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def wait_for_response(self, timeout=60):
        """
        Wait for ChatGPT's response.
        """
        try:
            # Wait for the "Stop generating" button to disappear
            self.wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='stop-generating-button']"))
            )
            
            # Wait a bit more to ensure the response is complete
            time.sleep(2)
            
            # Get the last response
            responses = self.driver.find_elements(By.CSS_SELECTOR, "div[data-message-author-role='assistant']")
            if responses:
                last_response = responses[-1].text
                logging.info("Response received")
                return True, last_response
            
            return False, "No response found"
            
        except Exception as e:
            error_msg = f"Error waiting for response: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def close(self):
        """
        Close the browser.
        """
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed")

def test_browser_controller():
    """
    Test function for the browser controller.
    """
    controller = BrowserController()
    
    try:
        # Initialize browser
        success, message = controller.initialize()
        if not success:
            print(f"Failed to initialize: {message}")
            return
        
        # Wait for user to log in
        print("Please log in to ChatGPT. Press Enter when ready...")
        input()
        
        # Send test message
        test_message = "Hello, this is a test message from the automation system."
        success, message = controller.send_message(test_message)
        if not success:
            print(f"Failed to send message: {message}")
            return
        
        # Wait for response
        success, response = controller.wait_for_response()
        if success:
            print("Response received:")
            print(response)
        else:
            print(f"Failed to get response: {response}")
        
    finally:
        controller.close()

if __name__ == "__main__":
    test_browser_controller() 