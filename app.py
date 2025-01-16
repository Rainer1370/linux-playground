from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import shlex

app = Flask(__name__, static_folder='static', template_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    try:
        command = data.get('cmd', '')
        # Whitelist of allowed commands for security
        allowed_commands = ['ls', 'pwd', 'echo', 'cat', 'whoami']
        if any(command.startswith(allowed) for allowed in allowed_commands):
            # Execute the command safely
            process = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            response = {
                'output': process.stdout or process.stderr
            }
        else:
            response = {
                'output': 'Command not allowed!'
            }
        emit('response', response)
    except Exception as e:
        emit('response', {'output': f'Error: {str(e)}'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
