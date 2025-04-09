from datetime import timedelta
from src.domain.services.user_service import UserService
from src.infrastructure.security import create_access_token, verify_password
from src.adapters.secondary.persistence.models.user_model import User

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate_user(self, email: str, password: str):
        user = self.user_service.get_user_by_email(email)
        if user and self.user_service.verify_user_password(user,password):
           return user
        return None

    def create_access_token_for_user(self, user):
        access_token_expires = timedelta(minutes=30)  # Configurar la expiración del token
        data = {
            'sub': user.id,          # ID del usuario
            'username': user.username,  # Nombre de usuario
            'role': user.role           # Rol del usuario
        }
        access_token = create_access_token(data=data, expires_delta=access_token_expires)
        return access_token
    

