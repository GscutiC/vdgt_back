from flask import Blueprint
from src.adapters.primary.http.controllers.user_controller import user_blueprint

# Registrar el blueprint de Usuarios 
usuarios_routes = Blueprint('usuarios_routes', __name__)
usuarios_routes.register_blueprint(user_blueprint, url_prefix='/usuarios') 