from flask import Blueprint
from src.adapters.primary.http.controllers.user_module import user_module

# Registrar el blueprint de autenticación
auth_routes = Blueprint('auth_routes', __name__)
auth_routes.register_blueprint(user_module, url_prefix='/auth') 