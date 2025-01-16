from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess

# Initialize Flask and SocketIO
app = Flask(__name__, static_folder='static', template_folder='.')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(data):
    try:
        command = data['command']
        # Run the command in a shell
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        if output:
            emit('response', {'output': output.decode('utf-8')})
        elif error:
            emit('response', {'output': error.decode('utf-8')})
    except Exception as e:
        emit('response', {'output': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
