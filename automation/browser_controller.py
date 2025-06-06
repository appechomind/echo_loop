#!/usr/bin/env python3
"""
Browser controller for ChatGPT automation
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import os

class BrowserController:
    """Controls browser interactions with ChatGPT."""
    
    def __init__(self, headless: bool = False, timeout: int = 30):
        self.driver = None
        self.headless = headless
        self.timeout = timeout
        self.wait = None
        
    def initialize(self) -> tuple[bool, str]:
        """Initialize the browser driver."""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Initialize Chrome driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            # Navigate to ChatGPT
            self.driver.get("https://chat.openai.com")
            logging.info("Browser initialized and navigated to ChatGPT")
            
            return True, "Browser initialized successfully"
            
        except WebDriverException as e:
            error_msg = f"Failed to initialize browser: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error during browser initialization: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def send_message(self, message: str) -> tuple[bool, str]:
        """Send a message to ChatGPT."""
        try:
            if not self.driver:
                return False, "Browser not initialized"
            
            # Wait for and find the message input area
            message_box = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
            
            # Clear and send message
            message_box.clear()
            message_box.send_keys(message)
            
            # Find and click send button
            send_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='send-button']"))
            )
            send_button.click()
            
            logging.info(f"Message sent: {message[:100]}...")
            return True, "Message sent successfully"
            
        except TimeoutException:
            error_msg = "Timeout waiting for ChatGPT interface elements"
            logging.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error sending message: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def wait_for_response(self, max_wait: int = 60) -> tuple[bool, str]:
        """Wait for and capture ChatGPT's response."""
        try:
            if not self.driver:
                return False, "Browser not initialized"
            
            # Wait for response to appear
            time.sleep(2)  # Initial wait
            
            start_time = time.time()
            while time.time() - start_time < max_wait:
                try:
                    # Look for response messages
                    response_elements = self.driver.find_elements(
                        By.XPATH, "//div[@data-message-author-role='assistant']//div[contains(@class, 'markdown')]"
                    )
                    
                    if response_elements:
                        # Get the latest response
                        latest_response = response_elements[-1].text
                        if latest_response.strip():
                            logging.info(f"Response received: {latest_response[:100]}...")
                            return True, latest_response
                    
                    time.sleep(1)
                    
                except Exception as e:
                    logging.warning(f"Error checking for response: {str(e)}")
                    time.sleep(1)
            
            error_msg = f"Timeout waiting for response after {max_wait} seconds"
            logging.error(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Error waiting for response: {str(e)}"
            logging.error(error_msg)
            return False, error_msg
    
    def get_conversation_history(self) -> list:
        """Get the current conversation history."""
        try:
            if not self.driver:
                return []
            
            messages = []
            
            # Get all message elements
            user_messages = self.driver.find_elements(
                By.XPATH, "//div[@data-message-author-role='user']"
            )
            assistant_messages = self.driver.find_elements(
                By.XPATH, "//div[@data-message-author-role='assistant']"
            )
            
            # Combine and sort by appearance order
            all_elements = user_messages + assistant_messages
            
            for element in all_elements:
                role = element.get_attribute("data-message-author-role")
                content = element.text.strip()
                if content:
                    messages.append({
                        "role": role,
                        "content": content,
                        "timestamp": time.time()
                    })
            
            return messages
            
        except Exception as e:
            logging.error(f"Error getting conversation history: {str(e)}")
            return []
    
    def close(self):
        """Close the browser."""
        try:
            if self.driver:
                self.driver.quit()
                logging.info("Browser closed")
        except Exception as e:
            logging.error(f"Error closing browser: {str(e)}")

def test_browser_controller():
    """Test function for the browser controller."""
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