from flask import jsonify, request
from app.services.event_service import EventService


class EventController:
    def __init__(self, db):
        self.event_service = EventService(db)

    def get_event(self):
        event_list = self.event_service.get_event_list()
        return jsonify({"code": 200, "message": "success", "data": event_list})

    def get_event_detail(self, event_id):
        event = self.event_service.get_event_by_id(event_id)
        if event:
            return jsonify({"code": 200, "message": "success", "data": event})
        else:
            return jsonify({"code": 404, "message": "Event not found"}), 404

    def post_event(self):
        print("post event")
        event_data = request.get_json()
        print("Received data:", event_data)
        if not event_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        event_id = self.event_service.add_event(event_data)
        return jsonify({"code": 200, "message": "Event added successfully", "data": {"event_id": event_id}})

    def update_event(self, event_id):
        print("update event")
        event_data = request.get_json()
        print("Received data:", event_data)
        if not event_data:
            return jsonify({"code": 400, "message": "No input data provided"}), 400
        self.event_service.update_event(event_id, event_data)
        return jsonify({"code": 200, "message": "Event updated successfully"})

    def delete_event(self, event_id):
        self.event_service.delete_event(event_id)
        return jsonify({"code": 200, "message": "Event deleted successfully"})
