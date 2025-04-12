from flask import Blueprint
from src.adapters.primary.http.controllers.auth_controller import auth_blueprint

# Registrar el blueprint de autenticación
auth_routes = Blueprint('auth_routes', __name__)
auth_routes.register_blueprint(auth_blueprint, url_prefix='/auth') 