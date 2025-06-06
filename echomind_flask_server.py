from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def index():
    # Serve the main UI
    return render_template("ui.html", log=get_latest_output())

@app.route("/api/prompt", methods=["POST"])
def api_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    if prompt:
        # Write the prompt to next_task.txt for the automation loop to pick up
        with open("next_task.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
        return jsonify({"status": "ok", "message": "Prompt received."})
    return jsonify({"status": "error", "message": "No prompt provided."}), 400

@app.route("/api/status", methods=["GET"])
def api_status():
    # Return the latest output from the AI/automation system
    return jsonify({"output": get_latest_output()})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def get_latest_output():
    # Try to read the latest output from ai_1_out.txt, ai_2_out.txt, ai_3_out.txt, or main_ai_output.py
    for fname in ["ai_3_out.txt", "ai_2_out.txt", "ai_1_out.txt", "main_ai_output.py"]:
        if os.path.exists(fname):
            try:
                with open(fname, "r", encoding="utf-8") as f:
                    return f.read()[-2000:]  # Return last 2000 chars for brevity
            except Exception:
                continue
    return "[No output yet]"

if __name__ == "__main__":
    app.run(port=8080, debug=True)