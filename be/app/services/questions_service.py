from bson.objectid import ObjectId
import paramiko
import logging
from config.config import Config

class QuestionsService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['questions']

    def get_all_questions(self):
        questions = list(self.collection.find({}, {'_id': 1, 'question': 1, 'options': 1, 'correctAnswer': 1, 'type': 1}))
        for item in questions:
            item['_id'] = str(item['_id'])
        return questions

    def check_answer(self, question_id, selected_option, check_type):
        question = self.collection.find_one({"_id": ObjectId(question_id)})
        if not question:
            return False
        
        if check_type == "multiple-choice":
            return question['correctAnswer'] == selected_option
        
        if check_type == "confirmation":
            # 动态生成和执行命令
            return self.check_confirmation_answer(question)

        return False

    def generate_command(self, template, parameters):
        """根据模板和参数生成命令"""
        if parameters:
            for key, value in parameters.items():
                placeholder = f"{{{key}}}"
                if placeholder in template:
                    template = template.replace(placeholder, value)
                else:
                    logging.warning(f"Placeholder {placeholder} not found in template.")
        else:
            logging.warning("No parameters provided for command generation.")
        
        logging.debug(f"Generated command: {template}")
        return template

    def execute_ssh_command(self, command):
        """连接SSH并执行命令"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(Config.MINIKUBE_VM_IP, username=Config.MINIKUBE_VM_USERNAME, key_filename=Config.MINIKUBE_SSH_KEY_PATH)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().strip()
            error = stderr.read().strip()
            
            if error:
                logging.error(f"Command execution error: {error.decode()}")
                return None
            
            return output.decode()

        except Exception as e:
            logging.error(f"SSH connection or command execution failed: {e}")
            return None

        finally:
            ssh.close()

    def check_confirmation_answer(self, question):
        if 'commandTemplate' not in question or 'parameters' not in question:
            logging.error("Missing command template or parameters in question.")
            return False

        # 使用命令模板和参数生成具体命令
        logging.debug(f"Question: {question}")
        command = self.generate_command(question['commandTemplate'], question.get('parameters'))
        logging.debug(f"Generated command: {command}")

        # 执行命令并获取结果
        output = self.execute_ssh_command(command)

        # 检查执行结果是否与正确答案匹配
        return output == question['correctAnswer']
