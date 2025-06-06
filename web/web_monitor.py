#!/usr/bin/env python3
"""
Web monitoring interface for EchoLoop automation system
"""

from flask import Flask, render_template, jsonify, request
import threading
import time
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.task_queue import TaskQueue, Task
import traceback

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Global variables for system state
system_state = {
    'status': 'stopped',
    'current_iteration': 0,
    'last_update': datetime.now(),
    'errors': [],
    'task_queue': None,
    'automation_thread': None
}

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('ui.html')

@app.route('/api/state')
def get_state():
    """Get current system state."""
    return jsonify({
        'status': system_state['status'],
        'current_iteration': system_state['current_iteration'],
        'last_update': system_state['last_update'].isoformat(),
        'errors': system_state['errors'][-10:],  # Last 10 errors
        'queue_stats': system_state['task_queue'].get_queue_stats() if system_state['task_queue'] else {}
    })

@app.route('/api/control', methods=['POST'])
def control_system():
    """Control system operations."""
    try:
        command = request.json.get('command')
        
        if command == 'start':
            return start_automation()
        elif command == 'stop':
            return stop_automation()
        elif command == 'pause':
            return pause_automation()
        elif command == 'resume':
            return resume_automation()
        elif command == 'status':
            return jsonify({'status': system_state['status']})
        else:
            return jsonify({'error': 'Unknown command'}), 400
            
    except Exception as e:
        logging.error(f"Control API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get recent log entries."""
    try:
        log_file = Path(__file__).parent.parent / 'logs' / 'loop.log'
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                lines = f.readlines()
                # Return last 50 lines
                return jsonify({'logs': lines[-50:]})
        else:
            return jsonify({'logs': []})
            
    except Exception as e:
        logging.error(f"Logs API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/<filename>')
def get_file_content(filename):
    """Get content of data files."""
    try:
        if filename not in ['ai_1_out.txt', 'ai_2_out.txt', 'ai_3_out.txt']:
            return jsonify({'error': 'File not allowed'}), 403
            
        file_path = Path(__file__).parent.parent / 'data' / filename
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({'content': content})
        else:
            return jsonify({'content': ''})
            
    except Exception as e:
        logging.error(f"File API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def start_automation():
    """Start the automation system."""
    try:
        if system_state['status'] == 'running':
            return jsonify({'message': 'System already running'})
        
        # Initialize task queue if not exists
        if not system_state['task_queue']:
            system_state['task_queue'] = TaskQueue(max_workers=2)
            system_state['task_queue'].start()
        
        system_state['status'] = 'running'
        system_state['last_update'] = datetime.now()
        
        # Start automation in background thread
        system_state['automation_thread'] = threading.Thread(
            target=automation_loop, 
            daemon=True
        )
        system_state['automation_thread'].start()
        
        logging.info("Automation system started")
        return jsonify({'message': 'System started successfully'})
        
    except Exception as e:
        error_msg = f"Failed to start system: {str(e)}"
        logging.error(error_msg)
        system_state['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'message': error_msg
        })
        return jsonify({'error': error_msg}), 500

def stop_automation():
    """Stop the automation system."""
    try:
        system_state['status'] = 'stopped'
        system_state['last_update'] = datetime.now()
        
        if system_state['task_queue']:
            system_state['task_queue'].stop()
            system_state['task_queue'] = None
        
        logging.info("Automation system stopped")
        return jsonify({'message': 'System stopped successfully'})
        
    except Exception as e:
        error_msg = f"Failed to stop system: {str(e)}"
        logging.error(error_msg)
        return jsonify({'error': error_msg}), 500

def pause_automation():
    """Pause the automation system."""
    if system_state['status'] == 'running':
        system_state['status'] = 'paused'
        system_state['last_update'] = datetime.now()
        logging.info("Automation system paused")
        return jsonify({'message': 'System paused'})
    else:
        return jsonify({'message': 'System not running'})

def resume_automation():
    """Resume the automation system."""
    if system_state['status'] == 'paused':
        system_state['status'] = 'running'
        system_state['last_update'] = datetime.now()
        logging.info("Automation system resumed")
        return jsonify({'message': 'System resumed'})
    else:
        return jsonify({'message': 'System not paused'})

def automation_loop():
    """Main automation loop running in background."""
    try:
        from core.echo_loop import process_iteration
        from automation.browser_controller import BrowserController
        
        # Initialize browser
        browser = BrowserController()
        if not browser.initialize():
            raise Exception("Failed to initialize browser")
        
        iteration = system_state['current_iteration']
        
        while system_state['status'] in ['running', 'paused']:
            try:
                if system_state['status'] == 'paused':
                    time.sleep(1)
                    continue
                
                # Create iteration task
                iteration_task = Task(
                    f"iteration_{iteration}",
                    process_iteration,
                    args=(browser, iteration),
                    max_retries=3,
                    retry_delay=5
                )
                
                # Add task to queue
                task_id = system_state['task_queue'].add_task(iteration_task, priority=1)
                
                # Wait for completion
                while True:
                    status = system_state['task_queue'].get_task_status(task_id)
                    if status['status'] in ['completed', 'failed']:
                        if status['status'] == 'failed':
                            error_msg = f"Iteration {iteration} failed: {status['error']}"
                            logging.error(error_msg)
                            system_state['errors'].append({
                                'timestamp': datetime.now().isoformat(),
                                'message': error_msg
                            })
                        else:
                            system_state['current_iteration'] = iteration
                            system_state['last_update'] = datetime.now()
                        break
                    time.sleep(1)
                
                iteration += 1
                time.sleep(2)  # Brief pause between iterations
                
            except Exception as e:
                error_msg = f"Error in automation loop: {str(e)}"
                logging.error(error_msg)
                system_state['errors'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': error_msg
                })
                time.sleep(5)  # Wait before retrying
        
        browser.close()
        
    except Exception as e:
        error_msg = f"Fatal error in automation loop: {str(e)}"
        logging.error(error_msg)
        system_state['errors'].append({
            'timestamp': datetime.now().isoformat(),
            'message': error_msg
        })
        system_state['status'] = 'error'

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("🌐 Starting EchoLoop Web Monitor...")
    print("📊 Access dashboard at: http://localhost:5000")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) 