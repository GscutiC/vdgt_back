from flask import Blueprint, request, jsonify
from src.adapters.secondary.external.face_recognition.face_recognit import DlibFaceRecognitionAdapter
from src.application.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.adapters.secondary.persistence.repositories.user_repository import UserRepository
from src.infrastructure.security import role_required
from src.adapters.secondary.persistence.models.user_model import User

auth_blueprint = Blueprint('auth', __name__)
face_recognizer = DlibFaceRecognitionAdapter()
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

@auth_blueprint.route("/register_face", methods=["POST"])
def register_face():
    data = request.form
    user = user_service.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        full_name=data["full_name"],
        role=data.get("role", "user"),
    )
    if 'face_image' in request.files:
        face_image = request.files['face_image'].read()
        try:
            success = face_recognizer.register_face(str(user.id), face_image)
            if not success:
                return jsonify({'message': 'Usuario registrado pero falló el registro facial'}), 201
        except Exception as e:
            return jsonify({'message': f'Usuario registrado pero falló el registro facial: {str(e)}'}), 201
    
    return jsonify({'message': 'Usuario registrado con éxito, incluido reconocimiento facial'}), 201

@auth_blueprint.route("/login_face", methods=["POST"])
def login_with_face():
    # Autenticar por rostro
    if 'face_image' not in request.files:
        return jsonify({'error': 'No se proporcionó imagen facial'}), 400
        
    face_image = request.files['face_image'].read()
    
    try:
        user_id = face_recognizer.authenticate_face(face_image)
        if not user_id:
            return jsonify({'error': 'Rostro no reconocido'}), 401
            
        # Buscar usuario por ID y generar token
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        access_token = auth_service.create_access_token_for_user(user)
        return jsonify({'access_token': access_token}), 200
            
    except Exception as e:
        return jsonify({'error': f'Error en autenticación facial: {str(e)}'}), 500