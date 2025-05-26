
import time
from cursor_agent import run_cursor_agent
from chatgpt_agent import run_chatgpt_agent
from llama3_agent import run_llama3_agent

CYCLE_DELAY = 5
GITHUB_PUSH_INTERVAL = 25

def log(message):
    with open("loop.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{time.ctime()}] {message}\n")

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
        log(f"✅ Iteration {iteration} complete.\n")
        iteration += 1

if __name__ == "__main__":
    main()
