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

class EchoLoopUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.loop_running = False
        self.loop_paused = False
        self.loop_thread = None
        self.last_user_message = None

    def init_ui(self):
        self.setWindowTitle('EchoMind AutoLoop')
        self.resize(900, 600)

        # Conversation display area
        self.conversation_area = QtWidgets.QTextEdit(self)
        self.conversation_area.setReadOnly(True)
        self.conversation_area.setPlaceholderText('Conversation will appear here...')

        # User input area
        self.input_box = QtWidgets.QLineEdit(self)
        self.input_box.setPlaceholderText('Type your idea or command here...')
        self.send_btn = QtWidgets.QPushButton('Send')

        # Control buttons
        self.start_btn = QtWidgets.QPushButton('Start')
        self.stop_btn = QtWidgets.QPushButton('Stop')
        self.pause_btn = QtWidgets.QPushButton('Pause')

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.conversation_area)
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.stop_btn)
        self.setLayout(layout)

        # Placeholder: Connect buttons to future automation logic
        self.start_btn.clicked.connect(self.start_loop)
        self.stop_btn.clicked.connect(self.stop_loop)
        self.pause_btn.clicked.connect(self.pause_loop)
        self.send_btn.clicked.connect(self.send_user_input)

    def start_loop(self):
        if not self.loop_running:
            self.loop_running = True
            self.loop_paused = False
            self.conversation_area.append('🔄 [System] Loop started.')
            self.loop_thread = threading.Thread(target=self.automation_loop, daemon=True)
            self.loop_thread.start()
        else:
            self.conversation_area.append('⚠️ [System] Loop already running.')

    def stop_loop(self):
        self.loop_running = False
        self.conversation_area.append('⏹️ [System] Loop stopped.')

    def pause_loop(self):
        self.loop_paused = not self.loop_paused
        state = 'paused' if self.loop_paused else 'resumed'
        self.conversation_area.append(f'⏸️ [System] Loop {state}.')

    def send_user_input(self):
        user_text = self.input_box.text().strip()
        if user_text:
            self.conversation_area.append(f'📝 [User]: {user_text}')
            self.last_user_message = user_text
            self.input_box.clear()

    def automation_loop(self):
        loop_count = 0
        while self.loop_running:
            if self.loop_paused:
                time.sleep(0.5)
                continue
            loop_count += 1
            # 1. Pull latest from GitHub
            self.update_ui('🔃 [Git] Pulling latest changes...')
            self.git_pull()
            # 2. Launch or focus ChatGPT in Chrome
            self.update_ui('🌐 [Browser] Ensuring ChatGPT is open...')
            self.ensure_chatgpt_open()
            # 3. Type message to ChatGPT
            message = self.last_user_message or f'Hello from Cursor! (loop {loop_count})'
            self.update_ui(f'⌨️ [Cursor] Typing to ChatGPT: {message}')
            self.type_to_chatgpt(message)
            # 4. Wait for response (1.5 min max)
            self.update_ui('⏳ [System] Waiting for ChatGPT response...')
            response = self.read_chatgpt_response(timeout=90)
            self.update_ui(f'🤖 [ChatGPT]: {response}')
            # 5. Cursor processes response, makes repo edits
            self.update_ui('🧠 [Cursor] Analyzing repo and making improvements...')
            self.cursor_process_response(response)
            # 6. Every 25 loops: log, create folder, push
            if loop_count % 25 == 0:
                self.update_ui('📦 [Git] Logging and pushing changes...')
                self.git_push(loop_count)
            # 7. Wait or break if stopped
            for _ in range(5):
                if not self.loop_running:
                    break
                time.sleep(1)

    def update_ui(self, text):
        QtCore.QMetaObject.invokeMethod(self.conversation_area, "append", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, text))

    def ensure_chatgpt_open(self):
        # Try to find Chrome window with ChatGPT, or launch if not found
        try:
            chatgpt_url = 'https://chat.openai.com/'
            chrome_windows = [w for w in gw.getWindowsWithTitle('Chrome') if w.isVisible]
            chatgpt_window = None
            for w in chrome_windows:
                if 'chat.openai.com' in w.title.lower() or 'chatgpt' in w.title.lower():
                    chatgpt_window = w
                    break
            if not chatgpt_window:
                webbrowser.open(chatgpt_url)
                time.sleep(5)  # Wait for Chrome to open
                chrome_windows = [w for w in gw.getWindowsWithTitle('Chrome') if w.isVisible]
                chatgpt_window = chrome_windows[0] if chrome_windows else None
            if chatgpt_window:
                chatgpt_window.activate()
                time.sleep(1)
                self.update_ui('✅ [Browser] ChatGPT window focused.')
            else:
                self.update_ui('❌ [Browser] Could not find or open ChatGPT window.')
        except Exception as e:
            self.update_ui(f'❌ [Browser] Error: {e}')

    def type_to_chatgpt(self, message):
        try:
            time.sleep(1)
            pyautogui.click()  # Focus input box (assumes it's focused)
            time.sleep(0.5)
            pyautogui.typewrite(message, interval=0.03)
            pyautogui.press('enter')
            self.update_ui('✅ [Cursor] Message sent to ChatGPT.')
        except Exception as e:
            self.update_ui(f'❌ [Cursor] Typing error: {e}')

    def read_chatgpt_response(self, timeout=90):
        # Wait for response, then OCR the response area
        start_time = time.time()
        last_text = ''
        while time.time() - start_time < timeout:
            # Screenshot a region (user may need to adjust these coordinates)
            x, y, w, h = 300, 200, 900, 500  # Example region
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            text = pytesseract.image_to_string(img)
            if text.strip() and text.strip() != last_text:
                last_text = text.strip()
                if len(last_text) > 10:  # Heuristic: response is ready
                    return last_text
            time.sleep(2)
        return last_text or '[No response detected]'

    def cursor_process_response(self, response):
        # Example: create a new file with the response
        try:
            filename = f'cursor_response_{int(time.time())}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response)
            self.update_ui(f'📄 [Cursor] Saved response to {filename}')
        except Exception as e:
            self.update_ui(f'❌ [Cursor] File write error: {e}')

    def git_pull(self):
        # Use subprocess to run 'git pull'
        try:
            subprocess.run(['git', 'pull'], check=True)
        except Exception as e:
            self.update_ui(f'❌ [Git] Pull failed: {e}')

    def git_push(self, loop_count):
        # Use subprocess to add, commit, and push
        try:
            folder_name = f'loop_{loop_count}'
            os.makedirs(folder_name, exist_ok=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', f'Auto-update at loop {loop_count}'], check=True)
            subprocess.run(['git', 'push'], check=True)
        except Exception as e:
            self.update_ui(f'❌ [Git] Push failed: {e}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = EchoLoopUI()
    win.show()
    sys.exit(app.exec_())
