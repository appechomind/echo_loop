import queue
import threading
import time
import logging
from datetime import datetime
from typing import Dict, Any, Callable, List, Optional
import traceback

# Set up logging
logging.basicConfig(
    filename='task_queue.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Task:
    def __init__(self, name: str, func: Callable, args: tuple = (), kwargs: dict = None,
                 max_retries: int = 3, retry_delay: int = 5, dependencies: List[str] = None):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.status = 'pending'
        self.result = None
        self.error = None
        self.retry_count = 0
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.dependencies = dependencies or []
        self.dependency_status = {dep: False for dep in self.dependencies}

class TaskQueue:
    def __init__(self, max_workers: int = 4):
        self.queue = queue.PriorityQueue()
        self.max_workers = max_workers
        self.workers = []
        self.running = False
        self.tasks: Dict[str, Task] = {}
        self.lock = threading.Lock()
        self.task_events: Dict[str, threading.Event] = {}
    
    def start(self):
        """Start the task queue workers."""
        if self.running:
            return
        
        self.running = True
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.workers.append(worker)
        
        logging.info(f"Started {self.max_workers} workers")
    
    def stop(self):
        """Stop the task queue workers."""
        self.running = False
        for worker in self.workers:
            worker.join()
        self.workers.clear()
        logging.info("Stopped all workers")
    
    def add_task(self, task: Task, priority: int = 0) -> str:
        """Add a task to the queue with priority."""
        with self.lock:
            task_id = f"{task.name}_{int(time.time())}"
            self.tasks[task_id] = task
            self.task_events[task_id] = threading.Event()
            self.queue.put((priority, task_id, task))
            logging.info(f"Added task: {task_id}")
            return task_id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task."""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return {'error': 'Task not found'}
            
            return {
                'name': task.name,
                'status': task.status,
                'created_at': task.created_at.isoformat(),
                'started_at': task.started_at.isoformat() if task.started_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'result': task.result,
                'error': str(task.error) if task.error else None,
                'retry_count': task.retry_count,
                'dependencies': task.dependencies,
                'dependency_status': task.dependency_status
            }
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get the status of all tasks."""
        with self.lock:
            return {
                task_id: self.get_task_status(task_id)
                for task_id in self.tasks
            }
    
    def _check_dependencies(self, task: Task) -> bool:
        """Check if all dependencies are completed."""
        return all(task.dependency_status.values())
    
    def _update_dependency_status(self, task_id: str, status: bool):
        """Update dependency status for dependent tasks."""
        with self.lock:
            for tid, task in self.tasks.items():
                if task_id in task.dependencies:
                    task.dependency_status[task_id] = status
                    if status and self._check_dependencies(task):
                        self.task_events[tid].set()
    
    def _worker_loop(self):
        """Worker loop that processes tasks from the queue."""
        while self.running:
            try:
                priority, task_id, task = self.queue.get(timeout=1)
                
                # Wait for dependencies
                if task.dependencies:
                    if not self._check_dependencies(task):
                        self.task_events[task_id].wait()
                
                self._process_task(task_id, task)
                self.queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error in worker loop: {str(e)}\n{traceback.format_exc()}")
    
    def _process_task(self, task_id: str, task: Task):
        """Process a single task with retries."""
        while task.retry_count <= task.max_retries:
            try:
                # Update task status
                with self.lock:
                    task.status = 'running'
                    task.started_at = datetime.now()
                
                # Execute task
                result = task.func(*task.args, **task.kwargs)
                
                # Update task status
                with self.lock:
                    task.status = 'completed'
                    task.completed_at = datetime.now()
                    task.result = result
                
                # Update dependency status
                self._update_dependency_status(task_id, True)
                
                logging.info(f"Completed task: {task_id}")
                return
                
            except Exception as e:
                task.retry_count += 1
                if task.retry_count > task.max_retries:
                    # Update task status
                    with self.lock:
                        task.status = 'failed'
                        task.completed_at = datetime.now()
                        task.error = e
                    
                    # Update dependency status
                    self._update_dependency_status(task_id, False)
                    
                    logging.error(f"Failed task: {task_id} - {str(e)}\n{traceback.format_exc()}")
                    return
                
                logging.warning(f"Retrying task {task_id} (attempt {task.retry_count}/{task.max_retries})")
                time.sleep(task.retry_delay)

# Example usage
if __name__ == "__main__":
    def example_task(name: str, delay: int):
        """Example task that sleeps for a specified duration."""
        time.sleep(delay)
        return f"Task {name} completed after {delay} seconds"
    
    # Create task queue
    task_queue = TaskQueue(max_workers=2)
    task_queue.start()
    
    # Add some tasks with dependencies
    task1 = Task("example1", example_task, args=("Task 1", 2))
    task2 = Task("example2", example_task, args=("Task 2", 3), dependencies=["example1_0"])
    task3 = Task("example3", example_task, args=("Task 3", 1), dependencies=["example1_0", "example2_0"])
    
    task_id1 = task_queue.add_task(task1)
    task_id2 = task_queue.add_task(task2)
    task_id3 = task_queue.add_task(task3)
    
    # Monitor tasks
    while True:
        status1 = task_queue.get_task_status(task_id1)
        status2 = task_queue.get_task_status(task_id2)
        status3 = task_queue.get_task_status(task_id3)
        
        print("\nTask Status:")
        print(f"Task 1: {status1['status']}")
        print(f"Task 2: {status2['status']}")
        print(f"Task 3: {status3['status']}")
        
        if all(status['status'] in ['completed', 'failed'] for status in [status1, status2, status3]):
            break
        
        time.sleep(1)
    
    # Stop task queue
    task_queue.stop() 