from flask import Blueprint, request, jsonify
from src.application.services.auth_service import AuthService
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.user_service import UserService
from src.infrastructure.security import role_required

login_blueprint = Blueprint('login', __name__)

# Inicializar servicios
user_repository = UserRepository()
user_service = UserService(user_repository)
auth_service = AuthService(user_service)


# Ruta para que el usuario pueda logiarse
@login_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = auth_service.authenticate_user(data['email'], data['password'])
    if user:
        access_token = auth_service.create_access_token_for_user(user)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }), 200
    return jsonify({'error': 'Invalid credentials'}), 401 

# Ruta para que el usuario o admin pueda cerrae sesion 
@login_blueprint.route('/logout', methods=['POST'])
def logout():
    
    return jsonify({'message': 'tu ya no tienes acceso '}), 200

# Ruta para que el admin pueda ingresar al dashboard de administracion
@login_blueprint.route('/admin-dashboard', methods=['GET'])
@role_required('admin')  # Usamos el decorador para restringir acceso solo a administradores
def admin_dashboard():
    return jsonify({
        'message': 'Bienvenido a la pagina de administracion',
        'admin_tools': ['Administrar usuarios', 'Ver registros', 'Administrar configuraciones']
    }), 200
