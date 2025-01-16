from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import os

app = Flask(__name__, static_folder='static', template_folder='.')
socketio = SocketIO(app)
python_shell = []

# Function to set up the environment
def setup_environment():
    try:
        # Update the system and install dependencies
        subprocess.run(
            "apt-get update && apt-get install -y python3 python3-pip git build-essential ca-certificates",
            shell=True,
            check=True,
        )
        # Install EPICS base if not already installed
        if not os.path.exists('/epics'):
            subprocess.run(
                "git clone --depth=1 https://github.com/epics-base/epics-base.git /epics",
                shell=True,
                check=True,
            )
            subprocess.run("make -C /epics", shell=True, check=True)
        print("Environment setup complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up environment: {e}")

# Run the setup during initialization
setup_environment()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_files', methods=['GET'])
def list_files():
    files = os.listdir('.')
    return {'files': files}

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join('.', file.filename))
    return 'File uploaded successfully!'

@socketio.on('command')
def handle_command(data):
    cmd = data['cmd']
    if cmd.startswith("python"):
        # Interactive Python shell
        try:
            exec_globals = {}
            exec_locals = {}
            exec(cmd[7:], exec_globals, exec_locals)
            result = exec_locals.get('result', 'Command executed')
            emit('response', {'output': str(result)})
        except Exception as e:
            emit('response', {'output': str(e)})
    elif cmd.startswith("epics"):
        # Handle EPICS commands
        try:
            epics_cmd = cmd[len("epics "):]  # Strip the "epics " prefix
            output = subprocess.check_output(epics_cmd, shell=True, stderr=subprocess.STDOUT)
            emit('response', {'output': output.decode('utf-8')})
        except subprocess.CalledProcessError as e:
            emit('response', {'output': e.output.decode('utf-8')})
    else:
        # Handle system commands
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            emit('response', {'output': output.decode('utf-8')})
        except subprocess.CalledProcessError as e:
            emit('response', {'output': e.output.decode('utf-8')})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
