from flask import Blueprint
from src.adapters.primary.http.controllers.face_controller import face_blueprint

# Registrar el blueprint de  Reconocimiento facial
face_routes = Blueprint('face_routes', __name__)
face_routes.register_blueprint(face_blueprint, url_prefix='/face') 