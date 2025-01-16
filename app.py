import os
import pty
import subprocess
import select
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

# Initialize Flask and SocketIO
app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)

@app.route("/")
def index():
    """Render the index.html template."""
    return render_template("index.html")

@socketio.on("input")
def handle_input(data):
    """
    Handle input from the terminal.
    Executes the given command and streams output back to the client.
    """
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
                close_fds=True,
                universal_newlines=True  # Ensures proper decoding of output
            )
            os.close(slave)
            
            while True:
                r, _, _ = select.select([master], [], [], 0.1)
                if r:
                    output = os.read(master, 1024).decode()
                    if output:
                        emit("output", {"output": output})
                    else:
                        break
            os.close(master)
        except Exception as e:
            emit("output", {"output": f"Error: {str(e)}"})
    else:
        emit("output", {"output": "No command provided."})

if __name__ == "__main__":
    # Run the Flask app with SocketIO
    socketio.run(app, host="0.0.0.0", port=5000)
