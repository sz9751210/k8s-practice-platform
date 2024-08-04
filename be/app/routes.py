from app.controllers.k8s_controller import K8sController
from app.controllers.questions_controller import QuestionsController

def setup_routes(app, client):

    # controllers
    k8s_controller = K8sController()
    question_controller = QuestionsController(client)
    
    api_prefix= '/api/devops'

    # k8s
    app.add_url_rule(f"{api_prefix}/k8s/deploy", view_func=k8s_controller.deploy, methods=['POST'])
    app.add_url_rule(f"{api_prefix}/k8s/reset", view_func=k8s_controller.reset, methods=['POST'])
    # app.add_url_rule(f"{api_prefix}/execute-command", view_func=k8s_controller.execute_command, methods=['POST'])
    
    # questions
    app.add_url_rule(f"{api_prefix}/questions", view_func=question_controller.get_questions, methods=['GET'])
    app.add_url_rule(f"{api_prefix}/check-answer", view_func=question_controller.check_answer, methods=['POST'])
    