from flask import Blueprint
from src.adapters.primary.http.controllers.password_controller import password_blueprint

# Registrar el blueprint de  Reset contraseña
password_routes = Blueprint('password_routes', __name__)
password_routes.register_blueprint(password_blueprint, url_prefix='/password') 