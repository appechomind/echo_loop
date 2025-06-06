from flask import Flask, render_template, jsonify, request
import threading
import time
import json
import logging
from datetime import datetime
import os
try:
    from task_queue import TaskQueue, Task
except ImportError:
    from core.task_queue import TaskQueue, Task
import traceback
import sys

# Set up logging
logging.basicConfig(
    filename='web_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Global state
automation_state = {
    'status': 'stopped',
    'current_step': '',
    'progress': 0,
    'iteration': 0,
    'last_update': datetime.now().isoformat(),
    'log_messages': [],
    'tasks': {},
    'error_count': 0,
    'success_count': 0,
    'total_iterations': 0
}

# Global task queue
task_queue = None

def update_state(status=None, current_step=None, progress=None, iteration=None, log_message=None, tasks=None,
                error_count=None, success_count=None, total_iterations=None):
    """Update the global state."""
    global automation_state
    if status:
        automation_state['status'] = status
    if current_step:
        automation_state['current_step'] = current_step
    if progress is not None:
        automation_state['progress'] = progress
    if iteration is not None:
        automation_state['iteration'] = iteration
    if log_message:
        automation_state['log_messages'].append({
            'timestamp': datetime.now().isoformat(),
            'message': log_message,
            'level': 'error' if 'error' in log_message.lower() else 'info'
        })
        # Keep only last 100 messages
        automation_state['log_messages'] = automation_state['log_messages'][-100:]
    if tasks is not None:
        automation_state['tasks'] = tasks
    if error_count is not None:
        automation_state['error_count'] = error_count
    if success_count is not None:
        automation_state['success_count'] = success_count
    if total_iterations is not None:
        automation_state['total_iterations'] = total_iterations
    automation_state['last_update'] = datetime.now().isoformat()

@app.route('/')
def index():
    """Render the main monitoring page."""
    return render_template('monitor.html')

@app.route('/ai_chat')
def ai_chat():
    """Render the AI chat interface."""
    return render_template('ai_chat.html')

# NEW: AI Conversation API endpoints
@app.route('/api/conversation')
def get_conversation():
    """Get the full AI conversation."""
    try:
        conversation = []
        
        # Read AI files in order
        ai_files = [
            ('ai_1_out.txt', 'Cursor Agent', '💡'),
            ('ai_2_out.txt', 'ChatGPT Agent', '💬'), 
            ('ai_3_out.txt', 'Gemini Agent', '🧠')
        ]
        
        for filename, agent_name, icon in ai_files:
            try:
                if os.path.exists(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            # Get file modification time
                            mod_time = datetime.fromtimestamp(os.path.getmtime(filename))
                            conversation.append({
                                'agent': agent_name,
                                'icon': icon,
                                'content': content,
                                'timestamp': mod_time.isoformat(),
                                'file': filename
                            })
            except Exception as e:
                logging.error(f"Error reading {filename}: {str(e)}")
                conversation.append({
                    'agent': agent_name,
                    'icon': icon,
                    'content': f"Error reading file: {str(e)}",
                    'timestamp': datetime.now().isoformat(),
                    'file': filename,
                    'error': True
                })
        
        return jsonify({'conversation': conversation})
        
    except Exception as e:
        logging.error(f"Error getting conversation: {str(e)}")
        return jsonify({'error': str(e)}), 500

# NEW: Send message to AI agents
@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Send a message/command to all AI agents."""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Create timestamp for the message
        timestamp = datetime.now().isoformat()
        
        # Write to user input file that AI agents can read
        user_input_file = 'user_input.txt'
        with open(user_input_file, 'w', encoding='utf-8') as f:
            f.write(f"[{timestamp}] User Command: {message}")
        
        # Also write to individual agent input files
        agent_files = ['ai_1_input.txt', 'ai_2_input.txt', 'ai_3_input.txt']
        for agent_file in agent_files:
            try:
                with open(agent_file, 'w', encoding='utf-8') as f:
                    f.write(f"[{timestamp}] User Command: {message}")
            except Exception as e:
                logging.error(f"Error writing to {agent_file}: {str(e)}")
        
        # Log the message
        update_state(log_message=f"User message sent to all agents: {message}")
        
        # Clear the AI output files to prepare for new responses
        output_files = ['ai_1_out.txt', 'ai_2_out.txt', 'ai_3_out.txt']
        for output_file in output_files:
            try:
                if os.path.exists(output_file):
                    # Keep a backup of the last message
                    backup_file = f"{output_file}.backup"
                    with open(output_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Clear the output file
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write("")
            except Exception as e:
                logging.error(f"Error clearing {output_file}: {str(e)}")
        
        return jsonify({
            'status': 'success',
            'message': 'Command sent to all AI agents',
            'timestamp': timestamp
        })
        
    except Exception as e:
        logging.error(f"Error sending message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/<filename>')
def get_conversation_file(filename):
    """Get content of a specific AI conversation file."""
    try:
        allowed_files = ['ai_1_out.txt', 'ai_2_out.txt', 'ai_3_out.txt']
        if filename not in allowed_files:
            return jsonify({'error': 'File not allowed'}), 403
            
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                mod_time = datetime.fromtimestamp(os.path.getmtime(filename))
                return jsonify({
                    'content': content,
                    'timestamp': mod_time.isoformat(),
                    'file': filename
                })
        else:
            return jsonify({
                'content': '',
                'timestamp': datetime.now().isoformat(),
                'file': filename
            })
            
    except Exception as e:
        logging.error(f"Error getting file {filename}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/state')
def get_state():
    """Get the current automation state."""
    try:
        if task_queue:
            # Convert tasks dictionary to array of task objects
            tasks = task_queue.get_all_tasks()
            task_list = []
            for task_id, task in tasks.items():
                task_list.append({
                    'id': task_id,
                    'name': task['name'],
                    'status': task['status'],
                    'created_at': task['created_at'],
                    'started_at': task['started_at'],
                    'completed_at': task['completed_at'],
                    'error': task['error'],
                    'retry_count': task['retry_count'],
                    'max_retries': task.get('max_retries', 3),
                    'dependencies': task.get('dependencies', []),
                    'dependency_status': task.get('dependency_status', {})
                })
            automation_state['tasks'] = task_list
        return jsonify(automation_state)
    except Exception as e:
        logging.error(f"Error getting state: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to get state',
            'details': str(e)
        }), 500

@app.route('/api/control', methods=['POST'])
def control():
    """Handle control commands."""
    try:
        command = request.json.get('command')
        if not command:
            return jsonify({'error': 'No command provided'}), 400
        
        if command == 'start':
            if automation_state['status'] == 'running':
                return jsonify({'error': 'Automation is already running'}), 400
            update_state(status='running', current_step='Initializing')
            threading.Thread(target=run_automation).start()
        elif command == 'stop':
            if automation_state['status'] == 'stopped':
                return jsonify({'error': 'Automation is already stopped'}), 400
            update_state(status='stopped', current_step='Stopped')
            if task_queue:
                task_queue.stop()
        elif command == 'pause':
            if automation_state['status'] != 'running':
                return jsonify({'error': 'Automation is not running'}), 400
            update_state(status='paused', current_step='Paused')
        elif command == 'resume':
            if automation_state['status'] != 'paused':
                return jsonify({'error': 'Automation is not paused'}), 400
            update_state(status='running', current_step='Resuming')
        else:
            return jsonify({'error': 'Invalid command'}), 400
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Error handling control command: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to handle command',
            'details': str(e)
        }), 500

def run_automation():
    """Run the automation process."""
    global task_queue
    
    try:
        # Initialize task queue
        task_queue = TaskQueue(max_workers=2)
        task_queue.start()
        update_state(log_message="Task queue initialized")
        
        # Simulate automation steps
        steps = [
            ('Initializing browser', 10),
            ('Reading input', 20),
            ('Sending message', 30),
            ('Waiting for response', 50),
            ('Processing response', 70),
            ('Writing changes', 90),
            ('Completing iteration', 100)
        ]
        
        error_count = 0
        success_count = 0
        total_iterations = 0
        
        while automation_state['status'] == 'running':
            try:
                for step, progress in steps:
                    if automation_state['status'] == 'stopped':
                        break
                    
                    update_state(current_step=step, progress=progress)
                    update_state(log_message=f"Executing: {step}")
                    
                    # Simulate work
                    time.sleep(2)
                
                if automation_state['status'] != 'stopped':
                    success_count += 1
                    total_iterations += 1
                    update_state(
                        success_count=success_count,
                        total_iterations=total_iterations,
                        log_message=f"Completed iteration {total_iterations}"
                    )
                
            except Exception as e:
                error_count += 1
                update_state(
                    error_count=error_count,
                    log_message=f"Error in iteration: {str(e)}\n{traceback.format_exc()}"
                )
        
        if automation_state['status'] != 'stopped':
            update_state(
                status='completed',
                current_step='Completed',
                progress=100,
                log_message="Automation completed successfully"
            )
        
    except Exception as e:
        update_state(
            status='error',
            current_step='Error',
            log_message=f"Fatal error: {str(e)}\n{traceback.format_exc()}"
        )
    finally:
        if task_queue:
            task_queue.stop()
            task_queue = None

if __name__ == '__main__':
    try:
        # Create templates directory if it doesn't exist
        os.makedirs('templates', exist_ok=True)
        
        # Create monitor.html template
        with open('templates/monitor.html', 'w', encoding='utf-8') as f:
            f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echo Loop Monitor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }
        .status {
            padding: 10px;
            border-radius: 4px;
            font-weight: bold;
        }
        .status.running { background-color: #d4edda; color: #155724; }
        .status.stopped { background-color: #f8d7da; color: #721c24; }
        .status.paused { background-color: #fff3cd; color: #856404; }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        .start { background-color: #28a745; color: white; }
        .stop { background-color: #dc3545; color: white; }
        .pause { background-color: #ffc107; color: black; }
        .resume { background-color: #17a2b8; color: white; }
        .progress-container {
            margin-bottom: 20px;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }
        .progress {
            width: 0%;
            height: 100%;
            background-color: #007bff;
            transition: width 0.3s ease;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        .task-queue {
            margin-bottom: 20px;
        }
        .task-list {
            list-style: none;
            padding: 0;
        }
        .task-item {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding: 15px;
            background-color: #f8f9fa;
            margin-bottom: 8px;
            border-radius: 4px;
            border: 1px solid #e9ecef;
        }
        .task-info {
            flex: 1;
            margin-right: 15px;
        }
        .task-name {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .task-details {
            font-size: 0.9em;
            color: #6c757d;
        }
        .task-time {
            display: block;
            margin: 2px 0;
        }
        .task-error {
            display: block;
            color: #dc3545;
            margin: 2px 0;
        }
        .task-retries {
            display: block;
            color: #ffc107;
            margin: 2px 0;
        }
        .task-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
        }
        .status-pending { background-color: #ffc107; color: black; }
        .status-running { background-color: #17a2b8; color: white; }
        .status-completed { background-color: #28a745; color: white; }
        .status-failed { background-color: #dc3545; color: white; }
        .log-container {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            height: 300px;
            overflow-y: auto;
        }
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-bottom: 1px solid #eee;
        }
        .log-time {
            color: #6c757d;
            font-size: 0.8em;
        }
        .log-message {
            margin-left: 10px;
        }
        .log-entry.error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        .task-dependencies {
            display: block;
            color: #6c757d;
            font-size: 0.9em;
            margin: 2px 0;
        }
        .task-error {
            display: block;
            color: #dc3545;
            margin: 2px 0;
            font-weight: bold;
        }
        .task-retries {
            display: block;
            color: #ffc107;
            margin: 2px 0;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Echo Loop Monitor</h1>
            <div id="status" class="status stopped">Stopped</div>
        </div>
        
        <div class="controls">
            <button class="start" onclick="sendCommand('start')">Start</button>
            <button class="stop" onclick="sendCommand('stop')">Stop</button>
            <button class="pause" onclick="sendCommand('pause')">Pause</button>
            <button class="resume" onclick="sendCommand('resume')">Resume</button>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div>Total Iterations</div>
                <div id="total-iterations" class="stat-value">0</div>
            </div>
            <div class="stat-card">
                <div>Success Rate</div>
                <div id="success-rate" class="stat-value">0%</div>
            </div>
            <div class="stat-card">
                <div>Error Count</div>
                <div id="error-count" class="stat-value">0</div>
            </div>
        </div>
        
        <div class="progress-container">
            <h3>Progress</h3>
            <div class="progress-bar">
                <div id="progress" class="progress"></div>
            </div>
        </div>
        
        <div class="task-queue">
            <h3>Task Queue</h3>
            <ul id="task-list" class="task-list"></ul>
        </div>
        
        <div class="log-container">
            <h3>Log Messages</h3>
            <div id="log-messages"></div>
        </div>
    </div>

    <script>
        function updateUI(data) {
            try {
                // Update status
                const status = document.getElementById('status');
                status.className = 'status ' + data.status;
                status.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
                
                // Update progress
                document.getElementById('progress').style.width = data.progress + '%';
                
                // Update stats
                document.getElementById('total-iterations').textContent = data.total_iterations;
                document.getElementById('success-rate').textContent = 
                    data.total_iterations > 0 ? 
                    Math.round((data.success_count / data.total_iterations) * 100) + '%' : 
                    '0%';
                document.getElementById('error-count').textContent = data.error_count;
                
                // Update task queue
                const taskList = document.getElementById('task-list');
                taskList.innerHTML = '';
                if (Array.isArray(data.tasks)) {
                    data.tasks.forEach(task => {
                        const li = document.createElement('li');
                        li.className = 'task-item';
                        li.innerHTML = `
                            <div class="task-info">
                                <div class="task-name">${task.name}</div>
                                <div class="task-details">
                                    <span class="task-time">Created: ${new Date(task.created_at).toLocaleString()}</span>
                                    ${task.started_at ? `<span class="task-time">Started: ${new Date(task.started_at).toLocaleString()}</span>` : ''}
                                    ${task.completed_at ? `<span class="task-time">Completed: ${new Date(task.completed_at).toLocaleString()}</span>` : ''}
                                    ${task.error ? `<span class="task-error">Error: ${task.error}</span>` : ''}
                                    ${task.retry_count > 0 ? `<span class="task-retries">Retries: ${task.retry_count}/${task.max_retries}</span>` : ''}
                                    ${task.dependencies.length > 0 ? `
                                        <span class="task-dependencies">
                                            Dependencies: ${task.dependencies.join(', ')}
                                        </span>
                                    ` : ''}
                                </div>
                            </div>
                            <span class="task-status status-${task.status}">${task.status}</span>
                        `;
                        taskList.appendChild(li);
                    });
                }
                
                // Update log messages
                const logMessages = document.getElementById('log-messages');
                data.log_messages.forEach(msg => {
                    const div = document.createElement('div');
                    div.className = 'log-entry';
                    div.innerHTML = `
                        <span class="log-time">[${msg.time}]</span>
                        <span class="log-message">${msg.message}</span>
                    `;
                    logMessages.appendChild(div);
                });
                logMessages.scrollTop = logMessages.scrollHeight;
            } catch (error) {
                console.error('Error updating UI:', error);
                // Show error in log messages
                const logMessages = document.getElementById('log-messages');
                const div = document.createElement('div');
                div.className = 'log-entry error';
                div.innerHTML = `
                    <span class="log-time">[${new Date().toLocaleString()}]</span>
                    <span class="log-message">Error updating UI: ${error.message}</span>
                `;
                logMessages.appendChild(div);
                logMessages.scrollTop = logMessages.scrollHeight;
            }
        }

        function sendCommand(command) {
            fetch('/api/control', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    // Show error in log messages
                    const logMessages = document.getElementById('log-messages');
                    const div = document.createElement('div');
                    div.className = 'log-entry error';
                    div.innerHTML = `
                        <span class="log-time">[${new Date().toLocaleString()}]</span>
                        <span class="log-message">Error: ${data.error}</span>
                    `;
                    logMessages.appendChild(div);
                    logMessages.scrollTop = logMessages.scrollHeight;
                }
            })
            .catch(error => {
                console.error('Error sending command:', error);
                // Show error in log messages
                const logMessages = document.getElementById('log-messages');
                const div = document.createElement('div');
                div.className = 'log-entry error';
                div.innerHTML = `
                    <span class="log-time">[${new Date().toLocaleString()}]</span>
                    <span class="log-message">Error sending command: ${error.message}</span>
                `;
                logMessages.appendChild(div);
                logMessages.scrollTop = logMessages.scrollHeight;
            });
        }

        // Poll for updates every second
        setInterval(() => {
            fetch('/api/state')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    updateUI(data);
                })
                .catch(error => {
                    console.error('Error fetching state:', error);
                    // Show error in log messages
                    const logMessages = document.getElementById('log-messages');
                    const div = document.createElement('div');
                    div.className = 'log-entry error';
                    div.innerHTML = `
                        <span class="log-time">[${new Date().toLocaleString()}]</span>
                        <span class="log-message">Error fetching state: ${error.message}</span>
                    `;
                    logMessages.appendChild(div);
                    logMessages.scrollTop = logMessages.scrollHeight;
                });
        }, 1000);
    </script>
</body>
</html>
            ''')
        
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logging.error(f"Failed to start web monitor: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1) 