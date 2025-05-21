from flask import Blueprint
from src.adapters.primary.http.controllers.user_controller import user_blueprint
from src.adapters.primary.http.controllers.login_controller import login_blueprint
from src.adapters.primary.http.controllers.face_controller import face_blueprint
from src.adapters.primary.http.controllers.password_controller import password_blueprint
from src.adapters.primary.http.controllers.mano_obra_controller import mano_obra_blueprint
from src.adapters.primary.http.controllers.resumen_controller import resumen_blueprint
from src.adapters.primary.http.controllers.ventana_controller import ventana_blueprint
from src.adapters.primary.http.controllers.ventana_material_controller import ventana_material_blueprint
from src.adapters.primary.http.controllers.material_controller import material_blueprint

user_module = Blueprint('user_module', __name__)
user_module.register_blueprint(user_blueprint)
user_module.register_blueprint(login_blueprint)
user_module.register_blueprint(face_blueprint)
user_module.register_blueprint(password_blueprint)
user_module.register_blueprint(mano_obra_blueprint)
user_module.register_blueprint(resumen_blueprint)
user_module.register_blueprint(ventana_blueprint)
user_module.register_blueprint(ventana_material_blueprint)
user_module.register_blueprint(material_blueprint)




