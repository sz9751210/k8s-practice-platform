from flask_socketio import emit, join_room, leave_room
from flask import request
import paramiko
from app import socketio
from config.config import Config

sessions = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'output': 'Connected to server\n'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    sid = request.sid
    if sid in sessions:
        sessions[sid]['ssh'].close()
        del sessions[sid]

@socketio.on('execute_command')
def handle_execute_command(data):
    sid = request.sid
    command = data.get('command')
    if command:
        if sid not in sessions:
            ssh, channel = setup_ssh_session()
            if not ssh or not channel:
                emit('response', {'output': 'SSH connection failed\n'}, room=sid)
                return
            sessions[sid] = {'ssh': ssh, 'channel': channel}
        else:
            channel = sessions[sid]['channel']
        print(f"Executing command: {command}")
        channel.send(command + '\n')


def setup_ssh_session():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(Config.MINIKUBE_VM_IP, username=Config.MINIKUBE_VM_USERNAME, key_filename=Config.MINIKUBE_SSH_KEY_PATH)
        channel = ssh.invoke_shell()
        channel.settimeout(0)
        print('SSH connection established')
        return ssh, channel
    except Exception as e:
        print(f"SSH connection failed: {e}")
        return None, None

@socketio.on('input')
def handle_input(data):
    sid = request.sid
    command = data['input']
    if sid in sessions:
        sessions[sid]['channel'].send(command)

@socketio.on('resize')
def handle_resize(data):
    sid = request.sid
    cols = data['cols']
    rows = data['rows']
    if sid in sessions:
        sessions[sid]['channel'].resize_pty(width=cols, height=rows)

def read_output():
    while True:
        for sid, session in sessions.items():
            if session['channel'].recv_ready():
                try:
                    output = session['channel'].recv(1024).decode()
                    socketio.emit('response', {'output': output}, room=sid)
                except Exception as e:
                    print(e)
        socketio.sleep(0.1)

socketio.start_background_task(target=read_output)