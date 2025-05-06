from datetime import timedelta
from typing import Optional
from src.domain.services.user_service import UserService
from src.infrastructure.security import create_access_token, verify_password
from src.adapters.secondary.persistence.models.user_model import User
import bcrypt

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
    
        user = self.user_service.get_user_by_email(email)
        
        if not user:
            return None
        
        # Verificar la contraseña - asegúrate de que este método exista en UserService
        if not self.user_service.verify_user_password(user, password):
            return None
        
        return user

    def create_access_token_for_user(self, user):
        access_token_expires = timedelta(minutes=30)  # Configurar la expiración del token
        data = {
            'sub': user.id,          # ID del usuario
            'username': user.username,  # Nombre de usuario
            'role': user.role           # Rol del usuario
        }
        access_token = create_access_token(data=data, expires_delta=access_token_expires)
        return access_token
    

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        user = self.user_service.get_user_by_id(user_id)
        return user


    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su correo electrónico."""
        user = self.user_service.get_user_by_email(email)
        return user


    def verify_user_password(self, user: User, password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con la del usuario."""
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = user.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    
    def hash_password(self, password: str) -> str:
        """Genera un hash seguro de la contraseña utilizando bcrypt."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()  # Genera un "salt" aleatorio para mayor seguridad
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')  # Devuelve el hash como una cadena
