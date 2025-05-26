import time
from cursor_agent import run_cursor_agent
from chatgpt_agent import run_chatgpt_agent
from llama3_agent import run_llama3_agent
from git import Repo

CYCLE_DELAY = 30
GITHUB_PUSH_INTERVAL = 25

def log(message):
    with open("loop.log", "a", encoding="utf-8") as f:
        f.write(f"[{time.ctime()}] {message}\n")

def main():
    iteration = 1
    while True:
        log(f"🔁 Starting iteration {iteration}")
        run_cursor_agent()
        time.sleep(CYCLE_DELAY)
        run_chatgpt_agent()
        time.sleep(CYCLE_DELAY)
        run_llama3_agent()
        time.sleep(CYCLE_DELAY)

        if iteration % GITHUB_PUSH_INTERVAL == 0:
            try:
                repo = Repo(".")
                repo.git.add(".")
                repo.index.commit(f"🤖 Auto-commit at iteration {iteration}")
                origin = repo.remote(name="origin")
                origin.push()
                log("📤 Changes pushed to GitHub.")
            except Exception as e:
                log(f"❌ GitHub push failed: {e}")

        log(f"✅ Iteration {iteration} complete.\n")
        iteration += 1

if __name__ == "__main__":
    main()