import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import logging
import paramiko
import os
from config.config import Config, get_client
from app.routes import setup_routes

# 設定日誌級別和格式
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

MINIKUBE_VM_IP = os.getenv('MINIKUBE_VM_IP')
MINIKUBE_VM_USERNAME = os.getenv('MINIKUBE_VM_USERNAME')
MINIKUBE_SSH_KEY_PATH = os.getenv('MINIKUBE_SSH_KEY_PATH')

if not MINIKUBE_VM_IP or not MINIKUBE_VM_USERNAME or not MINIKUBE_SSH_KEY_PATH:
    logging.error("SSH configuration is incomplete. Check environment variables.")

sessions = {}

@app.route('/')
def index():
    return "Terminal Server is running."

def initialize_ssh_connection():
    """
    Initialize SSH connection to the remote VM.
    This should be called once during app startup.
    """
    try:
        logging.info("Attempting to connect to SSH...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(MINIKUBE_VM_IP, username=MINIKUBE_VM_USERNAME, key_filename=MINIKUBE_SSH_KEY_PATH)
        logging.info(f"SSH connection established to {MINIKUBE_VM_IP} as {MINIKUBE_VM_USERNAME}")

        # Execute any startup command, e.g., minikube start
        # stdin, stdout, stderr = ssh.exec_command('minikube start')
        # stdout_output = stdout.read().decode()
        # stderr_output = stderr.read().decode()

        # if stdout_output:
        #     logging.info(f"minikube start output: {stdout_output}")
        # if stderr_output:
        #     logging.error(f"minikube start error: {stderr_output}")

        return ssh  # Return the SSH client if needed later
    except paramiko.AuthenticationException:
        logging.error("SSH authentication failed. Check your credentials.")
    except paramiko.SSHException as e:
        logging.error(f"SSH connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None

def setup_ssh_session():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(MINIKUBE_VM_IP, username=MINIKUBE_VM_USERNAME, key_filename=MINIKUBE_SSH_KEY_PATH)
        logging.info(f"SSH connection established to {MINIKUBE_VM_IP} as {MINIKUBE_VM_USERNAME}")

        channel = ssh.invoke_shell()
        channel.settimeout(0)
        
        return ssh, channel
    except paramiko.AuthenticationException:
        logging.error("SSH authentication failed. Check your credentials.")
    except paramiko.SSHException as e:
        logging.error(f"SSH connection failed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    return None, None

@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')
    sid = request.sid
    if sid in sessions:
        sessions[sid]['ssh'].close()
        del sessions[sid]

@socketio.on('execute_command')
def handle_execute_command(data):
    sid = request.sid
    command = data.get('command')
    if sid not in sessions:
        logging.info("No existing session, setting up new SSH session.")
        ssh, channel = setup_ssh_session()
        if ssh is None or channel is None:
            emit('response', {'output': 'Failed to setup SSH session\n'})
            logging.error("Failed to setup SSH session.")
            return
        sessions[sid] = {'ssh': ssh, 'channel': channel}
    channel = sessions[sid]['channel']
    if command:
        logging.debug(f"Executing command: {command}")
        channel.send(command + '\n')

@socketio.on('input')
def handle_input(data):
    sid = request.sid
    command = data['input']
    if sid in sessions:
        logging.debug(f"Input received: {command}")
        sessions[sid]['channel'].send(command)

@socketio.on('resize')
def handle_resize(data):
    sid = request.sid
    cols = data['cols']
    rows = data['rows']
    if sid in sessions:
        logging.debug(f"Resizing terminal to {cols} cols and {rows} rows")
        sessions[sid]['channel'].resize_pty(width=cols, height=rows)

def read_output():
    while True:
        for sid, session in sessions.items():
            if session['channel'].recv_ready():
                try:
                    output = session['channel'].recv(1024).decode()
                    socketio.emit('response', {'output': output}, room=sid)
                    logging.debug(f"Output sent to client: {output}")
                except Exception as e:
                    logging.error(f"Error reading output: {e}")
        socketio.sleep(0.1)

# 初始化 MongoDB 和 SSH 連接
try:
    client = get_client()
    logging.info('MongoDB client initialized')
    setup_routes(app, client)
except Exception as e:
    logging.error(f'Failed to initialize MongoDB client: {e}')

ssh_client = initialize_ssh_connection()

socketio.start_background_task(target=read_output)

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
