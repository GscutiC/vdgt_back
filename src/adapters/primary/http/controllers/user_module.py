from flask import Blueprint
from src.adapters.primary.http.controllers.user_controller import user_blueprint
from src.adapters.primary.http.controllers.login_controller import login_blueprint
from src.adapters.primary.http.controllers.face_controller import face_blueprint
from src.adapters.primary.http.controllers.password_controller import password_blueprint
from src.adapters.primary.http.controllers.proyecto_controller import proyecto_blueprint
# from src.adapters.primary.http.controllers.materials_controller import materials_blueprint

user_module = Blueprint('user_module', __name__)
user_module.register_blueprint(user_blueprint)
user_module.register_blueprint(login_blueprint)
user_module.register_blueprint(face_blueprint)
user_module.register_blueprint(password_blueprint)
user_module.register_blueprint(proyecto_blueprint)
# user_module.register_blueprint(materials_blueprint)




