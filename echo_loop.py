import os
import time
import subprocess
from datetime import datetime

# Files to evolve (start with index.html, README)
targets = ["index.html", "README.md"]
repo_path = os.getcwd()

def evolve_file(path):
    with open(path, "a") as f:
        f.write(f"\n<!-- Evolved at {datetime.now()} -->\n")

def git_commit_push():
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "🤖 Auto-evolution commit"])
    subprocess.call(["git", "push", "origin", "main"])

if __name__ == "__main__":
    while True:
        for file in targets:
            if os.path.exists(file):
                evolve_file(file)
            else:
                with open(file, "w") as f:
                    f.write(f"<!-- {file} created by EchoLoop -->")
        git_commit_push()
        time.sleep(300)