from typing import List, Optional
# from src.domain.entities.user import User
from sqlalchemy.orm import Session
from src.adapters.secondary.persistence.models.user_model import User  # Importar el modelo correcto


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
       
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
       
        return self.session.query(User).filter(User.email == email).first()

    def list_all(self) -> List[User]:
        # TODO: Implementar la lógica para listar todos los usuarios
        return self.session.query(User).all()

    def update(self, user: User) -> User:
        # TODO: Implementar la lógica para actualizar un usuario
        self.session.merge(user)
        self.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        # TODO: Implementar la lógica para eliminar un usuario
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
