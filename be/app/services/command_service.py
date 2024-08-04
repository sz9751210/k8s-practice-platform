# app/services/command_service.py

import paramiko
import logging
from config.config import Config

class CommandService:
    def __init__(self):
        self.ssh_client = None

    def connect(self):
        if not self.ssh_client:
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(
                    Config.MINIKUBE_VM_IP,
                    username=Config.MINIKUBE_VM_USERNAME,
                    key_filename=Config.MINIKUBE_SSH_KEY_PATH
                )
                logging.info("SSH connection established")
            except Exception as e:
                logging.error(f"Failed to establish SSH connection: {e}")
                self.ssh_client = None

    def execute_command(self, command):
        if not self.ssh_client:
            self.connect()

        if self.ssh_client:
            try:
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                return output, error
            except Exception as e:
                logging.error(f"Failed to execute command '{command}': {e}")
                return "", str(e)

    def close_connection(self):
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            logging.info("SSH connection closed")
