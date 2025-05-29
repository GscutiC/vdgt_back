from flask import Blueprint
from src.adapters.primary.http.controllers.login_controller import login_blueprint
# Registrar el blueprint de autenticación
auth_routes = Blueprint('auth_routes', __name__)
auth_routes.register_blueprint(login_blueprint, url_prefix='/auth') 