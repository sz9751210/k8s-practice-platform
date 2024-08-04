import paramiko
import os

def test_ssh_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            os.environ.get('MINIKUBE_VM_IP'),
            username=os.environ.get('MINIKUBE_VM_USERNAME'),
            key_filename=os.environ.get('MINIKUBE_SSH_KEY_PATH')
        )
        print("SSH connection successful")
    except Exception as e:
        print(f"SSH connection failed: {e}")
        exit(1)
    finally:
        ssh.close()

if __name__ == "__main__":
    test_ssh_connection()
