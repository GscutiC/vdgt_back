from datetime import timedelta
from src.domain.services.user_service import UserService
from src.infrastructure.security import create_access_token, verify_password

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def authenticate_user(self, email: str, password: str):
        user = self.user_service.get_user_by_email(email)
        if user and self.user_service.verify_user_password(user, password):
            return user
        return None

    def create_access_token_for_user(self, user):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
        return access_token
