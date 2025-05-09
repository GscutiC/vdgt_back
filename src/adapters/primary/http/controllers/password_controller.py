from flask import Blueprint, request, jsonify
from src.application.services.auth_service import AuthService
from src.application.services.email_service import send_email
from src.infrastructure.security import create_password_reset_token, verify_jwt
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.user_service import UserService

password_blueprint = Blueprint('password', __name__)

# Inicializar servicios
user_repository = UserRepository()
user_service = UserService(user_repository)
auth_service = AuthService(user_service)

@password_blueprint.route('/password-reset', methods=['POST'])
def password_reset_request():
    data = request.get_json()
    email = data.get('email')
    
    user = auth_service.get_user_by_email(email)  # Obtener usuario por correo
    
    if user:
        # Crear un token de recuperación de contraseña
        reset_token = create_password_reset_token({'sub': user.id})
        
        # Enviar el token por correo electrónico (simularemos el proceso)
        # Aquí agregarías el código para enviar el correo con el enlace

        # Enviar el token por correo electrónico
        send_email(
             user.email,
             'Recuperación de Contraseña',
             f'Para restablecer tu contraseña, haz clic en este enlace: http://localhost:3000/password-reset/{reset_token}'
        )
        
        return jsonify({
            "message": "Se ha enviado un enlace para restablecer tu contraseña al correo proporcionado.",
            "reset_token": reset_token 
        }), 200
    
    return jsonify({'error': 'Correo no registrado'}), 400

@password_blueprint.route('/password-reset/<token>', methods=['POST'])
def password_reset(token):
    data = request.get_json()
    new_password = data.get('new_password')
    
    # Verificar el token JWT
    user_data = verify_jwt(token)
    if 'error' in user_data:
        return jsonify(user_data), 401  # Token inválido o expirado
    
    user_id = user_data['sub']
    
    # Buscar al usuario
    user = auth_service.get_user_by_id(user_id)
    if user:
        # Actualizar la contraseña del usuario
        hashed_password = auth_service.hash_password(new_password)
        user.password = hashed_password
        user_repository.update_password(user)
        return jsonify({'message': 'Contraseña actualizada con éxito'}), 200
    
    return jsonify({'error': 'Usuario no encontrado'}), 404