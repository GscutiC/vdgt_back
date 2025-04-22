from typing import List, Optional
from src.adapters.secondary.persistence.models.user_model import User
from src.infrastructure.database import session_factory
from src.adapters.secondary.persistence.models.facial_embeding_model import FacialEmbedding
import bcrypt

class UserRepository:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def create_user(self, username: str, email: str, password: str, full_name: str, role: str = "user") -> User:
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

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None,
                    password: Optional[str] = None, full_name: Optional[str] = None, role: Optional[str] = None) -> Optional[User]:
        # Actualizar información de un usuario
        session = session_factory()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                if username:
                    user.username = username
                if email:
                    user.email = email
                if password:
                    user.password = password
                if full_name:
                    user.full_name = full_name
                if role:
                    user.role = role
                session.commit()
                session.refresh(user)
                return user
            return None
        except Exception as e:
            session.rollback()
            print(f"Error al actualizar usuario: {e}")
            raise
        finally:
            session.close()

    

    def list_all_users(self) -> List[User]:
        # Obtener todos los usuarios
        session = session_factory()
        try:
            return session.query(User).all()
        finally:
            session.close()

    
    def delete_user(self, user_id: int) -> bool:
        session = session_factory()
        try:
        # Eliminar registros en la tabla facial_embeddings relacionados con el usuario
           facial_embeddings = session.query(FacialEmbedding).filter(FacialEmbedding.user_id == user_id).all()
           for embedding in facial_embeddings:
               session.delete(embedding)
        
          # Luego, eliminar el usuario
           user = session.query(User).filter(User.id == user_id).first()
           if user:
            session.delete(user)
            session.commit()
            return True
           return False
        except Exception as e:
          session.rollback()
          print(f"Error al eliminar usuario: {e}")
          raise
        finally:
          session.close()