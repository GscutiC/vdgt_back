from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from src.infrastructure.config import SECRET_KEY
from functools import wraps
from flask import request, jsonify

# Configuración de la seguridad
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Función para verificar la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Función para generar un hash de la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    
    # Asegúrate de que el campo 'sub' sea una cadena
    if 'sub' in to_encode and not isinstance(to_encode['sub'], str):
        to_encode['sub'] = str(to_encode['sub'])
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt

# Función para verificar un token JWT
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "El token ha expirado"}
    except jwt.JWTError as e:
        return {"error": f"Error al decodificar el token: {str(e)}"}

def role_required(required_role):
    """
    Decorador para verificar que el usuario tiene el rol necesario.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')  # Obtener el token de la cabecera
            if not token:
                return jsonify({'error': 'Falta el token'}), 401

            # Verificar si el token tiene el prefijo "Bearer"
            if token.startswith("Bearer "):
                token = token.split(" ")[1]  # Eliminar el prefijo "Bearer"

            try:
                # Verificar y decodificar el token JWT
                user_data = verify_jwt(token)  # Decodificar el JWT y obtener los datos del usuario
                if not isinstance(user_data, dict) or "error" in user_data:
                    return jsonify({'error': user_data.get("error", "El token no es válido")}), 401

                user_role = user_data.get('role')  # Obtener el rol del usuario desde el JWT
                if user_role != required_role:
                    return jsonify({
                        'error': 'Acceso denegado',
                        'message': f'Solo {required_role} puede acceder a este recurso',
                        'user_role': user_role,
                        'token_payload': user_data   # Mostrar el rol del usuario para depuración
                    }), 403
            except Exception as e:
                return jsonify({'error': f'Error inesperado: {str(e)}'}), 401

            return f(*args, **kwargs)  # Si todo está bien, proceder con la función original

        return wrapper
    return decorator