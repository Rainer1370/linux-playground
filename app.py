import os
import pty
import subprocess
import select
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app)

@app.route("/")
def index():
    # Serve index.html from the root directory
    return send_from_directory(os.getcwd(), "index.html")

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
            emit("output", {"output": f"Error: {str(e)}"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
