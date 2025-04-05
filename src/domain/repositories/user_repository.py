from typing import List, Optional
from src.domain.entities.user import User

class UserRepository:
    def save(self, user: User) -> User:
        # TODO: Implementar la lógica para guardar un usuario en la base de datos
        pass

    def get_by_id(self, user_id: int) -> Optional[User]:
        # TODO: Implementar la lógica para obtener un usuario por su ID
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        # TODO: Implementar la lógica para obtener un usuario por su email
        pass

    def list_all(self) -> List[User]:
        # TODO: Implementar la lógica para listar todos los usuarios
        pass

    def update(self, user: User) -> User:
        # TODO: Implementar la lógica para actualizar un usuario
        pass

    def delete(self, user_id: int) -> bool:
        # TODO: Implementar la lógica para eliminar un usuario
        pass
