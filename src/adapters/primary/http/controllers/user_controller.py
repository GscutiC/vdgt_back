from flask import Blueprint, request, jsonify
from src.domain.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security import role_required

user_blueprint = Blueprint('user', __name__)

# Inicializar servicios
user_repository = UserRepository()
user_service = UserService(user_repository)

# Ruta registrar un usuario 
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = user_service.create_user(
            username=data['username'],
            email=data['email'], 
            password=data['password'],
            full_name=data['full_name'],
            role=data.get('role', 'user')
        )
        if user:
            return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'error': 'Error al registrar el usuario'}), 400

# Ruta para obtener un usuario por su ID
@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role
        }), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

# Ruta para actualizar la información de un usuario
@user_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = user_repository.update_user(
        user_id,
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        full_name=data.get('full_name'),
        role=data.get('role')
    )
    if user:
        return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404


# Ruta para eliminar un usuario
@user_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = user_repository.delete_user(user_id)
    if success:
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

# Ruta para listar todos los usuarios
@user_blueprint.route('/users', methods=['GET'])
@role_required('admin')  # Aseguramos que solo los administradores puedan ver todos los usuarios
def list_users():
    users = user_repository.list_all_users()
    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role
    } for user in users]
    return jsonify(users_data), 200