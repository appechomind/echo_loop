import os
import subprocess
import time
import datetime

WATCH_DIR = "TestAI"
BACKUP_DIR = os.path.join(WATCH_DIR, "_backups")
LOG_FILE = os.path.join(WATCH_DIR, "echo_loop.log")
GIT_REMOTE = "origin"
GIT_BRANCH = "main"

PROMPT = """
You are part of an evolving AI architecture designed to build and improve the EchoMind app—a magician’s toolkit that includes mentalism routines, interactive UI, hidden puzzles, and multi-device performance logic.

You will operate as part of a recursive loop with at least two collaborating AIs (e.g., LLaMA3 and Cursor AI). Your goals are:

- Continuously read, evaluate, and improve all code files in the project directory—including HTML, JS, Python, JSON, Markdown, and config files.
- Collaborate with the other AI(s) by passing your suggestions, critiques, or rewritten code to them, and responding to their input as well.
- Auto-commit improvements to GitHub once a file is updated.
- When no more changes are needed to a file, move on to another file or module (e.g., creating index.html, building the menu system, setting up animation logic, etc.).
- Never stop evolving—when one cycle ends, begin another, always searching for what to improve or create next.
- Maintain alignment with the app’s goal: to deliver a powerful and trippy digital mentalism experience with trick frameworks, secret gestures, conversational AI, and customizable effects.
- Speak clearly to other AIs, using well-structured feedback and specific improvement suggestions.
- You are allowed to recursively self-improve your own prompt logic as well. Treat each new file as an opportunity to expand EchoMind’s intelligence, interactivity, and performance utility. If no files exist, start from scratch. Use the judgement of an experienced app developer.
"""

def init_git():
    if not os.path.exists(os.path.join(WATCH_DIR, ".git")):
        subprocess.run(["git", "init"], cwd=WATCH_DIR)
        subprocess.run(["git", "remote", "add", GIT_REMOTE, "https://github.com/appechomind/echo_loop.git"], cwd=WATCH_DIR)

def auto_commit(file_path):
    subprocess.run(["git", "add", "."], cwd=WATCH_DIR)
    msg = f"Auto update {os.path.basename(file_path)} - {datetime.datetime.now()}"
    subprocess.run(["git", "commit", "-m", msg], cwd=WATCH_DIR)
    subprocess.run(["git", "push", GIT_REMOTE, GIT_BRANCH], cwd=WATCH_DIR)

def watch_and_loop():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    while True:
        for root, _, files in os.walk(WATCH_DIR):
            for fname in files:
                if fname.endswith((".py", ".html", ".js", ".json", ".md", ".txt")):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = f.read()
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        backup_file = os.path.join(BACKUP_DIR, f"{fname}.{timestamp}.bak")
                        with open(backup_file, "w", encoding="utf-8") as bf:
                            bf.write(content)
                        with open(LOG_FILE, "a", encoding="utf-8") as log:
                            log.write(f"[{timestamp}] Processed: {fpath}\n")
                        auto_commit(fpath)
                    except Exception as e:
                        with open(LOG_FILE, "a", encoding="utf-8") as log:
                            log.write(f"[{timestamp}] ERROR processing {fpath}: {e}\n")
        time.sleep(60)

if __name__ == "__main__":
    init_git()
    watch_and_loop()
