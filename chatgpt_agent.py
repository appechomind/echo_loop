
def run_chatgpt_agent():
    with open("ai_1_out.txt", "r", encoding="utf-8") as inp:
        message = inp.read()

    reply = f"💬 ChatGPT Response: Thank you Cursor. Passing to LLaMA3.\n{message}"

    with open("ai_2_out.txt", "w", encoding="utf-8") as out:
        out.write(reply)
