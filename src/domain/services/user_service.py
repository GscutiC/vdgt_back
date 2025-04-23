from typing import List, Optional
# from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security import get_password_hash, verify_password
from src.adapters.secondary.persistence.models.user_model import User
import bcrypt
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    # Revisa este método en UserService
    def create_user(self, username, email, password, full_name, role="user"):
        print(f"Creando usuario: {username}, {email}")
        try:
            # Llamar al repositorio para crear al usuario
            user = self.user_repository.create_user(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                role=role
            )
            print(f"Usuario creado: {user}, ID: {user.id if user else 'None'}")
            return user
        except Exception as e:
            print(f"Error en UserService.create_user: {e}")
            raise

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)

    def list_all_users(self) -> List[User]:
        return self.user_repository.list_all()

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if user:
            user.update(**kwargs)
            return self.user_repository.update(user)
        return None

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)

    def verify_user_password(self, user: User, password: str) -> bool:
        """Verificar si la contraseña proporcionada coincide con la del usuario."""
        # Convertir la contraseña a bytes
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = user.password.encode('utf-8') 
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)   

