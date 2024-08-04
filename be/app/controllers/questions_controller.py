from flask import jsonify, request
from app.services.questions_service import QuestionsService
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class QuestionsController:
    def __init__(self, db):
        self.questions_service = QuestionsService(db)

    def get_questions(self):
        questions = self.questions_service.get_all_questions()
        return jsonify(questions)
    
    def check_answer(self):
        data = request.get_json()
        logging.info("check answer data", data)
        question_id = data.get('questionId')
        selected_option = data.get('selectedOption')
        check_type = data.get('checkType')

        if question_id is None or check_type is None:
            return jsonify({"error": "Invalid request data"}), 400

        is_correct = self.questions_service.check_answer(question_id, selected_option, check_type)

        return jsonify({"isCorrect": is_correct})
    