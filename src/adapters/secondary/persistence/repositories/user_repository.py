from typing import List, Optional
from src.domain.entities.user import User
from src.adapters.secondary.persistence.models.user_model import User as UserModel
from src.infrastructure.database import get_db
from src.infrastructure.database import session_factory
class UserRepository:
    def save(self, user: User) -> User:
        db = next(get_db())
        user_model = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            role=user.role  
        )
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return user

    def create_user(self, username, email, password, full_name, role="user"):
        print(f"Creando usuario: {username}, {email}, {full_name}")
        
        user = User(
            username=username,
            email=email,
            password=self.hash_password(password),
            full_name=full_name,
            role=role
        )
        
        print(f"Objeto user creado: {user.__dict__}")
        
        session = session_factory()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"Usuario guardado en DB. ID generado: {user.id}, tipo: {type(user.id)}")
            return user
        except Exception as e:
            session.rollback()
            print(f"Error al crear usuario: {e}")
            import traceback
            print(traceback.format_exc())
            raise
        finally:
            session.close()

    def get_by_id(self, user_id: int) -> Optional[User]:
        db = next(get_db())
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                full_name=user_model.full_name,
                is_active=user_model.is_active,
                role=user_model.role 
            )
        return None

    def get_by_email(self, email: str) -> Optional[User]:
        db = next(get_db())
        user_model = db.query(UserModel).filter(UserModel.email == email).first()
        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                full_name=user_model.full_name,
                is_active=user_model.is_active,
                role=user_model.role
            )
        return None

    def list_all(self) -> List[User]:
        db = next(get_db())
        user_models = db.query(UserModel).all()
        return [
            User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                full_name=user_model.full_name,
                is_active=user_model.is_active,
                role=user_model.role 
            )
            for user_model in user_models
        ]

    def update(self, user: User) -> User:
        db = next(get_db())
        user_model = db.query(UserModel).filter(UserModel.id == user.id).first()
        if user_model:
            user_model.username = user.username
            user_model.email = user.email
            user_model.hashed_password = user.hashed_password
            user_model.full_name = user.full_name
            user_model.is_active = user.is_active
            user_model.role = user.role 
            db.commit()
            db.refresh(user_model)
        return user

    def delete(self, user_id: int) -> bool:
        db = next(get_db())
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model:
            db.delete(user_model)
            db.commit()
            return True
        return False 