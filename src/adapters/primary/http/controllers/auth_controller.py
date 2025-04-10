from flask import Blueprint, request, jsonify
from src.application.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.adapters.secondary.persistence.repositories.user_repository import UserRepository
from src.infrastructure.security import role_required
from src.adapters.secondary.persistence.models.user_model import User

auth_blueprint = Blueprint('auth', __name__)

# Inicializar servicios
user_repository = UserRepository()
user_service = UserService(user_repository)
auth_service = AuthService(user_service)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = user_service.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        full_name=data['full_name'],
        role=data.get('role', 'user')
    )
    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'error': 'User registration failed'}), 400

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = auth_service.authenticate_user(data['email'], data['password'])
    if user:
        access_token = auth_service.create_access_token_for_user(user)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401 


# Endpoint para super usuario (admin) con funcionalidades adicionales
@auth_blueprint.route('/admin-dashboard', methods=['GET'])
@role_required('admin')  # Usamos el decorador para restringir acceso solo a administradores
def admin_dashboard():
    return jsonify({
        'message': 'Bienvenido a la pagina de administracion',
        'admin_tools': ['Administrar usuarios', 'Ver registros', 'Administrar configuraciones']
    }), 200

    
@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    
    return jsonify({'message': 'tu ya no tienes acceso '}), 200

