from flask import jsonify, request
from app.services.k8s_service import K8sService

class K8sController:
    def __init__(self):
        self.k8s_service = K8sService()

    def deploy(self):
        data = request.get_json()
        config = data.get('config')  # 確保 'config' 鍵存在
        if not config:
            return jsonify({"code": 400, "message": "Config not provided"}), 400
        
        output, error = self.k8s_service.deploy(config)
        if error:
            return jsonify({"code": 500, "message": "Deployment failed", "error": error}), 500
        return jsonify({"code": 200, "message": "Deployment successful", "output": output})

    def reset(self):
        output, error = self.k8s_service.reset()
        if error:
            return jsonify({"code": 500, "message": "Reset failed", "error": error}), 500
        return jsonify({"code": 200, "message": "Reset successful", "output": output})
