# Uses pytesseract to extract screen text for OCR

import pyautogui
import pytesseract
import cv2
import numpy as np
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='screen_reader.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def capture_screen():
    """
    Captures screen content and performs OCR to extract text.
    Returns the extracted text and the capture timestamp.
    """
    try:
        # 1. Capture screen content
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().isoformat()
        
        # Convert to OpenCV format
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # 2. Preprocess image for better OCR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # 3. Perform OCR
        text = pytesseract.image_to_string(thresh)
        
        # 4. Log the capture
        logging.info(f"Screen captured at {timestamp}")
        logging.info(f"Text length: {len(text)} characters")
        
        return {
            'text': text,
            'timestamp': timestamp,
            'success': True
        }
        
    except Exception as e:
        error_msg = f"Error in capture_screen: {str(e)}"
        logging.error(error_msg)
        return {
            'text': '',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': error_msg
        }

def capture_region(x, y, width, height):
    """
    Captures a specific region of the screen and performs OCR.
    """
    try:
        # 1. Capture specific region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        timestamp = datetime.now().isoformat()
        
        # Convert to OpenCV format
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # 2. Preprocess image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # 3. Perform OCR
        text = pytesseract.image_to_string(thresh)
        
        # 4. Log the capture
        logging.info(f"Region captured at {timestamp}")
        logging.info(f"Region: ({x}, {y}, {width}, {height})")
        logging.info(f"Text length: {len(text)} characters")
        
        return {
            'text': text,
            'timestamp': timestamp,
            'success': True
        }
        
    except Exception as e:
        error_msg = f"Error in capture_region: {str(e)}"
        logging.error(error_msg)
        return {
            'text': '',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': error_msg
        }

if __name__ == "__main__":
    # Test full screen capture
    result = capture_screen()
    print(f"Full screen capture: {'Success' if result['success'] else 'Failed'}")
    print(f"Text length: {len(result['text'])} characters")
    
    # Test region capture
    region_result = capture_region(0, 0, 800, 600)
    print(f"Region capture: {'Success' if region_result['success'] else 'Failed'}")
    print(f"Text length: {len(region_result['text'])} characters")
