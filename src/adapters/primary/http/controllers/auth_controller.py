from flask import Blueprint, request, jsonify
from src.adapters.secondary.external.face_recognition.face_recognit import DlibFaceRecognitionAdapter
from src.application.services.auth_service import AuthService
from src.domain.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository
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