from flask import Flask, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/execute/<command>")
def execute_command(command):
    allowed_commands = ["ls", "pwd", "whoami"]  # Define allowed commands
    if command not in allowed_commands:
        return "<pre>Command not allowed!</pre>"
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return f"<pre>{output}</pre>"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
