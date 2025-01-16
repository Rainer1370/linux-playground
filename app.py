import os
import pty
import subprocess
import select
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@socketio.on("input")
def handle_input(data):
    command = data.get("command")
    if command:
        try:
            master, slave = pty.openpty()
            process = subprocess.Popen(
                command,
                shell=True,
                stdin=slave,
                stdout=slave,
                stderr=slave,
                close_fds=True
            )
            os.close(slave)
            output = b""
            while True:
                r, _, _ = select.select([master], [], [], 0.1)
                if r:
                    chunk = os.read(master, 1024)
                    if chunk:
                        output += chunk
                        emit("output", {"output": chunk.decode()})
                    else:
                        break
            os.close(master)
        except Exception as e:
            emit("output", {"output": f"Error executing command: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
