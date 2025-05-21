import os
import subprocess
import time
import datetime

REPO_PATH = os.getcwd()
GITHUB_REPO = "https://github.com/appechomind/echo_loop.git"

PROMPT = """
You are part of an evolving AI architecture designed to build and improve the EchoMind app—a magician’s toolkit that includes mentalism routines, interactive UI, hidden puzzles, and multi-device performance logic.

You operate in a recursive loop with multiple AIs (LLaMA3, Cursor, etc.). Your responsibilities:

1. Continuously evaluate and improve all code in this repo: HTML, JS, CSS, Python, JSON, Markdown, etc.
2. Collaborate by debating improvements and responding to each other’s changes.
3. Auto-commit meaningful changes.
4. When finished with one task, pick or create another.
5. Build the index.html UI, submenus, animations, and magic trick logic.
6. Recursively improve your own reasoning.

Always evolve. Never stop. Your mission is to make EchoMind magical, immersive, and mind-blowing.
"""

def git_auto_commit():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "🔁 EchoLoop auto-evolve commit"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Auto-pushed to GitHub.")
    except subprocess.CalledProcessError:
        print("⚠️ Git commit or push skipped (likely no changes).")

def main_loop():
    print("🔁 EchoLoop Recursive AI Builder is now running...")
    print(f"🧠 Prompt loaded:
{PROMPT.strip()}")
    while True:
        print(f"
[{datetime.datetime.now().strftime('%H:%M:%S')}] Running evolution cycle...")
        git_auto_commit()
        # Simulate AI collaboration
        print("🤖 LLaMA3: Reviewing files...")
        print("✍️ Cursor AI: Rewriting and enhancing...")
        time.sleep(60)  # Wait before next cycle

if __name__ == "__main__":
    main_loop()