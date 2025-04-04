import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask, jsonify
from flask_cors import CORS
from src.application.middleware import request_logger
from src.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})

    # Register middleware
    app.before_request(request_logger)

    # Routes
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)