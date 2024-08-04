import paramiko
from config.config import Config

def execute_remote_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(Config.MINIKUBE_VM_IP, username=Config.MINIKUBE_VM_USERNAME, key_filename=Config.MINIKUBE_SSH_KEY_PATH)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()
    return output, error
