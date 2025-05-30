from flask import Blueprint
from src.adapters.primary.http.controllers.proyecto_controller import proyecto_blueprint

# Registrar el blueprint de Proyectos, materiales, cotización, optimizacion
proyecto_routes = Blueprint('proyecto_routes', __name__)
proyecto_routes.register_blueprint(proyecto_blueprint, url_prefix='/proyecto') 