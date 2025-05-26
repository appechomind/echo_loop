from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

template = '''
<!DOCTYPE html>
<html>
<head><title>EchoMind UI</title></head>
<body>
<h1>EchoMind Loop Control</h1>
<form method="post" action="/start"><button>▶ Start Loop</button></form>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(template)

@app.route("/start", methods=["POST"])
def start():
    subprocess.Popen(["python", "echo_loop.py"])
    return "Loop Started"

if __name__ == "__main__":
    app.run(port=8080)