import os
import time
import logging
from datetime import datetime
from browser_controller import BrowserController
from chatgpt_typer import type_with_retry
from screen_reader import capture_screen
from file_writer import write_changes
from gemini_agent import run_gemini_agent
import git
from task_queue import TaskQueue, Task
import traceback

# Set up logging
logging.basicConfig(
    filename='loop.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialize_git():
    """Initialize git repository if not already initialized."""
    try:
        repo = git.Repo('.')
        logging.info("Git repository already initialized")
    except git.InvalidGitRepositoryError:
        repo = git.Repo.init('.')
        logging.info("Initialized new git repository")
    return repo

def commit_and_push(repo, message="Automated commit"):
    """Commit changes and push to GitHub."""
    try:
        repo.index.add('*')
        repo.index.commit(message)
        origin = repo.remote('origin')
        origin.push()
        logging.info(f"Successfully committed and pushed changes: {message}")
        return True
    except Exception as e:
        logging.error(f"Error committing changes: {str(e)}\n{traceback.format_exc()}")
        return False

def read_input():
    """Read input from ai_1_out.txt."""
    try:
        with open('ai_1_out.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"Error reading input: {str(e)}\n{traceback.format_exc()}")
        raise

def save_response(response):
    """Save response to ai_2_out.txt."""
    try:
        with open('ai_2_out.txt', 'w', encoding='utf-8') as f:
            f.write(response)
        return True
    except Exception as e:
        logging.error(f"Error saving response: {str(e)}\n{traceback.format_exc()}")
        return False

def process_iteration(browser, iteration):
    """Process a single iteration of the automation loop."""
    try:
        # Read input
        input_text = read_input()
        if not input_text:
            raise ValueError("No input text found")
        
        # Send message to ChatGPT
        browser.send_message(input_text)
        
        # Wait for response
        response = browser.wait_for_response()
        if not response:
            raise ValueError("No response received from ChatGPT")
        
        # Save response
        if not save_response(response):
            raise ValueError("Failed to save response")
        
        # Run Gemini agent
        if not run_gemini_agent():
            raise ValueError("Gemini agent failed")
        
        # Capture screen
        screen_data = capture_screen()
        if not screen_data.get('success'):
            raise ValueError(f"Screen capture failed: {screen_data.get('error')}")
        
        # Type response
        if not type_with_retry(response):
            raise ValueError("Failed to type response")
        
        # Write changes
        if not write_changes():
            raise ValueError("Failed to write changes")
        
        logging.info(f"Completed iteration {iteration}")
        return True
    except Exception as e:
        logging.error(f"Error in iteration {iteration}: {str(e)}\n{traceback.format_exc()}")
        return False

def main():
    """Main automation loop."""
    # Initialize git
    repo = initialize_git()
    
    # Initialize task queue
    task_queue = TaskQueue(max_workers=2)
    task_queue.start()
    
    # Initialize browser
    browser = BrowserController()
    if not browser.initialize():
        logging.error("Failed to initialize browser")
        return
    
    iteration = 0
    last_commit_iteration = 0
    
    try:
        while True:
            try:
                # Create tasks for this iteration
                iteration_task = Task(
                    f"iteration_{iteration}",
                    process_iteration,
                    args=(browser, iteration),
                    max_retries=3,
                    retry_delay=5
                )
                
                # Add iteration task with high priority
                iteration_task_id = task_queue.add_task(iteration_task, priority=1)
                
                # Wait for iteration task completion
                while True:
                    status = task_queue.get_task_status(iteration_task_id)
                    if status['status'] in ['completed', 'failed']:
                        if status['status'] == 'failed':
                            logging.error(f"Iteration {iteration} failed: {status['error']}")
                            # Retry the entire iteration
                            continue
                        break
                    time.sleep(1)
                
                # Commit and push every 25 iterations
                if iteration - last_commit_iteration >= 25:
                    commit_task = Task(
                        f"commit_{iteration}",
                        commit_and_push,
                        args=(repo, f"Automated commit - iteration {iteration}"),
                        max_retries=2,
                        retry_delay=10
                    )
                    commit_task_id = task_queue.add_task(commit_task, priority=0)
                    
                    # Wait for commit task completion
                    while True:
                        status = task_queue.get_task_status(commit_task_id)
                        if status['status'] in ['completed', 'failed']:
                            if status['status'] == 'completed':
                                last_commit_iteration = iteration
                            break
                        time.sleep(1)
                
                iteration += 1
                
            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt, stopping...")
                break
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}\n{traceback.format_exc()}")
                time.sleep(5)  # Wait before retrying
    
    finally:
        # Cleanup
        task_queue.stop()
        browser.close()
        logging.info("Automation loop stopped")

if __name__ == "__main__":
    main()