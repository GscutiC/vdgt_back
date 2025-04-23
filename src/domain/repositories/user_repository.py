from typing import List, Optional
from src.adapters.secondary.persistence.models.user_model import User
from src.infrastructure.database import session_factory
import bcrypt

class UserRepository:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def create_user(self, username, email, password, full_name, role="user"):
        # Primero hash la contraseña
        hashed_password = self.hash_password(password)
        
        # Crear objeto usuario - usa 'hashed_password' en lugar de 'password'
        user = User(
            username=username,
            email=email,
            password=hashed_password,  # Asegúrate que este campo existe en User
            full_name=full_name,
            role=role
        )
        
        # Usar fábrica de sesiones
        session = session_factory()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"Usuario creado con ID: {user.id}")
            return user
        except Exception as e:
            session.rollback()
            print(f"Error al crear usuario: {e}")
            raise
        finally:
            session.close()
    
    # Resto de métodos adaptados al patrón de fábrica
    def get_by_id(self, user_id: int) -> Optional[User]:
        session = session_factory()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()
    
    def get_by_email(self, email: str) -> Optional[User]:
        session = session_factory()
        try:
            # Consulta a la base de datos para buscar el usuario por email
            user = session.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            print(f"Error al buscar usuario por email: {e}")
            return None
        finally:
            session.close()

    # ... otros métodos