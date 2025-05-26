def run_llama3_agent():
    with open("ai_2_out.txt", "r", encoding="utf-8") as f:
        chatgpt_input = f.read()
    with open("ai_1_out.txt", "w", encoding="utf-8") as out:
        out.write("LLaMA3 says: Generated fresh index.html. Returning to Cursor.\n")
