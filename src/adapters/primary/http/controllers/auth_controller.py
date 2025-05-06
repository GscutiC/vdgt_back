from flask import Blueprint, request, jsonify
from src.adapters.secondary.external.face_recognition.face_recognit import DlibFaceRecognitionAdapter
from src.application.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security import role_required
from src.adapters.secondary.persistence.models.user_model import User
from src.infrastructure.security import create_password_reset_token, verify_jwt
from src.application.services.email_service import send_email

auth_blueprint = Blueprint('auth', __name__)
face_recognizer = DlibFaceRecognitionAdapter()
# Inicializar servicios
user_repository = UserRepository()
user_service = UserService(user_repository)
auth_service = AuthService(user_service)

@auth_blueprint.route('/register', methods=['POST'])
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
@auth_blueprint.route('/user/<int:user_id>', methods=['GET'])
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
@auth_blueprint.route('/user/<int:user_id>', methods=['PUT'])
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
@auth_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = user_repository.delete_user(user_id)
    if success:
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404

# Ruta para listar todos los usuarios
@auth_blueprint.route('/users', methods=['GET'])
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


@auth_blueprint.route('/login', methods=['POST'])
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
    try:
        print("Iniciando register_face")
        if 'face_image' not in request.files:
            return jsonify({'error': 'No se proporcionó imagen facial'}), 400
            
        data = request.form
        print(f"Datos recibidos: {data}")
        
        # Validar datos requeridos
        required_fields = ["username", "email", "password", "full_name"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Falta el campo {field}"}), 400
        
        try:
            user = user_service.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                full_name=data["full_name"],
                role=data.get("role", "user"),
            )
        except Exception as e:
            return jsonify({'error': f'Error al crear usuario: {str(e)}'}), 500
        
        if not user:
            return jsonify({'error': 'Error al crear usuario: usuario nulo'}), 500
            
        print(f"ID del usuario: {user.id}, tipo: {type(user.id)}")
            
        if not user.id:
            return jsonify({'error': 'Error al crear usuario: no se generó ID'}), 500
            
        user_id = str(user.id) if user.id else None
        if not user_id:
            return jsonify({'error': 'ID de usuario inválido'}), 500
            
        print(f"ID de usuario para reconocimiento facial: {user_id}")
        
        face_image = request.files['face_image'].read()
        
        try:
            success = face_recognizer.register_face(user_id, face_image)
        except Exception as e:
            import traceback
            print(f"Error en reconocimiento facial: {e}")
            print(traceback.format_exc())
            return jsonify({
                'message': f'Usuario registrado pero falló el registro facial: {str(e)}',
                'user_id': user_id
            }), 201
        
        if success:
            return jsonify({
                'message': 'Usuario registrado con éxito, incluido reconocimiento facial',
                'user_id': user_id
            }), 201
        else:
            return jsonify({
                'message': 'Usuario registrado pero falló el registro facial',
                'user_id': user_id
            }), 201
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR EN REGISTRO: {str(e)}\n{error_trace}")
        return jsonify({'error': f'Error en el registro: {str(e)}'}), 500

@auth_blueprint.route("/login_face", methods=["POST"])
def login_face():
    try:
        # Verificar si hay imagen facial
        if 'face_image' not in request.files:
            return jsonify({'error': 'No se proporcionó imagen facial'}), 400
            
        face_image = request.files['face_image'].read()
        print("Iniciando proceso de login facial")
        
        # Identificar al usuario por su rostro
        user_id = face_recognizer.identify_face(face_image, threshold=0.6)
        
        if not user_id:
            print("No se pudo identificar al usuario por su rostro")
            return jsonify({
                'error': 'No se pudo identificar al usuario', 
                'details': 'No se encontró una coincidencia con suficiente confianza'
            }), 401
        
        print(f"Usuario identificado por rostro, ID: {user_id}")
        
        # Obtener el usuario
        user = user_service.get_user_by_id(int(user_id))
        
        if not user:
            print(f"Usuario con ID {user_id} no encontrado en la base de datos")
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Generar token
        access_token = auth_service.create_access_token_for_user(user)
        print(f"Login facial exitoso para usuario: {user.username}")
        
        return jsonify({
            'message': 'Login facial exitoso',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }), 200
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR EN LOGIN FACIAL: {str(e)}\n{error_trace}")
        return jsonify({'error': f'Error en login facial: {str(e)}'}), 500
    
@auth_blueprint.route('/password-reset', methods=['POST'])
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

@auth_blueprint.route('/password-reset/<token>', methods=['POST'])
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
