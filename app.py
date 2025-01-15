from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__, static_folder='static', template_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    try:
        output = subprocess.check_output(data['cmd'], shell=True, stderr=subprocess.STDOUT)
        emit('response', {'output': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        emit('response', {'output': e.output.decode('utf-8')})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
