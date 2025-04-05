from flask import Blueprint, request, jsonify
from src.application.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.adapters.secondary.persistence.repositories.user_repository import UserRepository

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
        full_name=data['full_name']
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