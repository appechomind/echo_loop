# PyQt GUI for EchoMind AutoLoop
# Handles conversation display, controls, and update logs
from PyQt5 import QtWidgets, QtCore
import sys
import threading
import time
import pyautogui
import pytesseract
import subprocess
import os
import webbrowser
import pygetwindow as gw
from PIL import ImageGrab
import logging
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                            QProgressBar, QTabWidget, QSplitter, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QTextCursor, QColor, QPalette

# Set up logging
logging.basicConfig(
    filename='gui.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AutomationThread(QThread):
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.paused = False
    
    def run(self):
        self.running = True
        self.paused = False
        iteration = 0
        
        while self.running:
            if not self.paused:
                try:
                    # Update status
                    self.status_signal.emit("Running")
                    
                    # Simulate automation steps
                    steps = [
                        "Reading input...",
                        "Sending to ChatGPT...",
                        "Processing response...",
                        "Running Gemini agent...",
                        "Applying changes...",
                        "Committing to Git..."
                    ]
                    
                    for i, step in enumerate(steps):
                        if not self.running or self.paused:
                            break
                        
                        self.update_signal.emit(f"Step {i+1}/{len(steps)}: {step}")
                        self.progress_signal.emit(int((i + 1) * 100 / len(steps)))
                        time.sleep(2)  # Simulate work
                    
                    iteration += 1
                    self.update_signal.emit(f"Completed iteration {iteration}")
                    
                except Exception as e:
                    self.update_signal.emit(f"Error: {str(e)}")
                    logging.error(f"Error in automation thread: {str(e)}")
            
            time.sleep(0.1)
    
    def stop(self):
        self.running = False
        self.status_signal.emit("Stopped")
    
    def pause(self):
        self.paused = True
        self.status_signal.emit("Paused")
    
    def resume(self):
        self.paused = False
        self.status_signal.emit("Running")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EchoLoop Automation System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Main tab
        main_tab = QWidget()
        main_layout = QVBoxLayout(main_tab)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Top section - Controls
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        
        # Control buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_automation)
        controls_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_automation)
        self.stop_button.setEnabled(False)
        controls_layout.addWidget(self.stop_button)
        
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_automation)
        self.pause_button.setEnabled(False)
        controls_layout.addWidget(self.pause_button)
        
        # Status label
        self.status_label = QLabel("Status: Stopped")
        controls_layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        controls_layout.addWidget(self.progress_bar)
        
        splitter.addWidget(controls_widget)
        
        # Middle section - Log display
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        
        log_label = QLabel("Automation Log")
        log_layout.addWidget(log_label)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display)
        
        splitter.addWidget(log_widget)
        
        # Bottom section - File operations
        file_widget = QWidget()
        file_layout = QHBoxLayout(file_widget)
        
        self.input_file_button = QPushButton("Select Input File")
        self.input_file_button.clicked.connect(self.select_input_file)
        file_layout.addWidget(self.input_file_button)
        
        self.output_file_button = QPushButton("Select Output File")
        self.output_file_button.clicked.connect(self.select_output_file)
        file_layout.addWidget(self.output_file_button)
        
        splitter.addWidget(file_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([100, 400, 100])
        
        tabs.addTab(main_tab, "Main")
        
        # Settings tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        
        # Add settings controls here
        settings_label = QLabel("Settings")
        settings_layout.addWidget(settings_label)
        
        tabs.addTab(settings_tab, "Settings")
        
        # Initialize automation thread
        self.automation_thread = AutomationThread()
        self.automation_thread.update_signal.connect(self.update_log)
        self.automation_thread.progress_signal.connect(self.update_progress)
        self.automation_thread.status_signal.connect(self.update_status)
        
        # Set dark theme
        self.set_dark_theme()
    
    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(palette)
    
    def start_automation(self):
        self.automation_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.update_log("Starting automation...")
    
    def stop_automation(self):
        self.automation_thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.update_log("Stopping automation...")
    
    def pause_automation(self):
        if self.automation_thread.paused:
            self.automation_thread.resume()
            self.pause_button.setText("Pause")
        else:
            self.automation_thread.pause()
            self.pause_button.setText("Resume")
    
    def update_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")
        self.log_display.moveCursor(QTextCursor.End)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        self.status_label.setText(f"Status: {status}")
    
    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "Text Files (*.txt)")
        if file_name:
            self.update_log(f"Selected input file: {file_name}")
    
    def select_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "Text Files (*.txt)")
        if file_name:
            self.update_log(f"Selected output file: {file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
