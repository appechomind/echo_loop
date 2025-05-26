from flask import Flask, request, render_template_string
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def ui():
    log = open("loop.log", "r", encoding="utf-8").read()
    return render_template_string(open("templates/ui.html").read(), log=log)
if __name__ == "__main__":
    app.run(port=8080)
