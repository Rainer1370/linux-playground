from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__, static_folder='static', template_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    cmd = data['cmd']
    try:
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if stdout:
            emit('response', {'output': stdout.decode('utf-8')})
        if stderr:
            emit('response', {'output': stderr.decode('utf-8')})
    except Exception as e:
        emit('response', {'output': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
