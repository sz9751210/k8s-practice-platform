import paramiko
from config.config import Config

class K8sService:
    def __init__(self):
        self.ssh_client = None

    def _connect(self):
        if not self.ssh_client:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                Config.MINIKUBE_VM_IP, 
                username=Config.MINIKUBE_VM_USERNAME, 
                key_filename=Config.MINIKUBE_SSH_KEY_PATH
            )

    def _execute_command(self, command):
        self._connect()
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output, error

    def deploy(self, config):
        # command = f"kubectl apply -f {config}"
        command = "kubectl create deployment --image=nginx nginx"
        return self._execute_command(command)

    def reset(self):
        command = "minikube delete && minikube start"
        return self._execute_command(command)
