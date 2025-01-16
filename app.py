from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import os

app = Flask(__name__, static_folder='static', template_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    cmd = data['cmd']
    try:
        # Execute the command in a shell
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output, error = process.communicate()
        response = output if output else error
        emit('response', {'output': response})
    except Exception as e:
        emit('response', {'output': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
