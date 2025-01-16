import os
import pty
import subprocess
import select
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("input")
def handle_input(data):
    command = data.strip()
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
                        emit("output", chunk.decode())
                    else:
                        break
            os.close(master)
        except Exception as e:
            emit("output", f"Error: {str(e)}\n")

@socketio.on("connect")
def connect_handler():
    print("Client connected")

@socketio.on("disconnect")
def disconnect_handler():
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
