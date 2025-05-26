def run_chatgpt_agent():
    with open("ai_1_out.txt", "r", encoding="utf-8") as f:
        cursor_input = f.read()
    with open("ai_2_out.txt", "w", encoding="utf-8") as out:
        out.write("ChatGPT says: Got the scan. Suggest cleaning HTML and linking index.html. Passing to LLaMA3.\n")
