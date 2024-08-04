from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from app.routes import setup_routes
import logging
import eventlet
import eventlet.wsgi
import app.controllers.terminal_controller

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# set up routes
setup_routes(app)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
