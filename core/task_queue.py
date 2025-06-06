#!/usr/bin/env python3
"""
Task queue system for EchoLoop automation
"""

import queue
import threading
import time
import logging
from datetime import datetime
from typing import Dict, Any, Callable, List, Optional
import traceback

class Task:
    """Represents a task in the queue."""
    
    def __init__(self, task_id: str, func: Callable, args: tuple = (), kwargs: dict = None, 
                 max_retries: int = 3, retry_delay: int = 5, priority: int = 0):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.priority = priority
        self.attempts = 0
        self.status = 'pending'
        self.result = None
        self.error = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None

class TaskQueue:
    """Thread-safe task queue with retry mechanism."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.queue = queue.PriorityQueue()
        self.workers = []
        self.tasks = {}  # task_id -> Task
        self.running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start the worker threads."""
        self.running = True
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, name=f"TaskWorker-{i}")
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
        logging.info(f"Started {self.max_workers} task workers")
    
    def stop(self):
        """Stop all worker threads."""
        self.running = False
        # Put sentinel values to wake up workers
        for _ in self.workers:
            self.queue.put((float('inf'), None))
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
        
        logging.info("Stopped all task workers")
    
    def add_task(self, task: Task, priority: int = 0) -> str:
        """Add a task to the queue."""
        task.priority = priority
        with self.lock:
            self.tasks[task.task_id] = task
            # Lower priority number = higher priority
            self.queue.put((priority, task))
        
        logging.info(f"Added task {task.task_id} with priority {priority}")
        return task.task_id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task."""
        with self.lock:
            if task_id not in self.tasks:
                return {'status': 'not_found'}
            
            task = self.tasks[task_id]
            return {
                'status': task.status,
                'attempts': task.attempts,
                'max_retries': task.max_retries,
                'created_at': task.created_at,
                'started_at': task.started_at,
                'completed_at': task.completed_at,
                'result': task.result,
                'error': str(task.error) if task.error else None
            }
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        with self.lock:
            pending = sum(1 for task in self.tasks.values() if task.status == 'pending')
            running = sum(1 for task in self.tasks.values() if task.status == 'running')
            completed = sum(1 for task in self.tasks.values() if task.status == 'completed')
            failed = sum(1 for task in self.tasks.values() if task.status == 'failed')
            
            return {
                'queue_size': self.queue.qsize(),
                'pending': pending,
                'running': running,
                'completed': completed,
                'failed': failed,
                'total_tasks': len(self.tasks)
            }
    
    def _worker_loop(self):
        """Worker loop that processes tasks from the queue."""
        while self.running:
            try:
                # Get task from queue (blocking with timeout)
                try:
                    priority, task = self.queue.get(timeout=1)
                    if task is None:  # Sentinel value
                        break
                except queue.Empty:
                    continue
                
                # Execute the task
                self._execute_task(task)
                
            except Exception as e:
                logging.error(f"Worker error: {str(e)}\n{traceback.format_exc()}")
    
    def _execute_task(self, task: Task):
        """Execute a single task with retry logic."""
        task.attempts += 1
        task.started_at = datetime.now()
        task.status = 'running'
        
        logging.info(f"Executing task {task.task_id} (attempt {task.attempts}/{task.max_retries})")
        
        try:
            # Execute the task function
            result = task.func(*task.args, **task.kwargs)
            
            # Task completed successfully
            task.result = result
            task.status = 'completed'
            task.completed_at = datetime.now()
            
            logging.info(f"Task {task.task_id} completed successfully")
            
        except Exception as e:
            logging.error(f"Task {task.task_id} failed: {str(e)}")
            task.error = e
            
            # Check if we should retry
            if task.attempts < task.max_retries:
                # Schedule retry
                task.status = 'pending'
                time.sleep(task.retry_delay)
                
                # Re-add to queue with same priority
                self.queue.put((task.priority, task))
                logging.info(f"Retrying task {task.task_id} in {task.retry_delay} seconds")
                
            else:
                # Max retries exceeded
                task.status = 'failed'
                task.completed_at = datetime.now()
                logging.error(f"Task {task.task_id} failed permanently after {task.attempts} attempts")

def create_task(task_id: str, func: Callable, args: tuple = (), kwargs: dict = None,
                max_retries: int = 3, retry_delay: int = 5) -> Task:
    """Convenience function to create a task."""
    return Task(task_id, func, args, kwargs, max_retries, retry_delay) 