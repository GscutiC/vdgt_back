from typing import List, Optional
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security import get_password_hash, verify_password

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str, password: str, full_name: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(id=None, username=username, email=email, hashed_password=hashed_password, full_name=full_name)
        return self.user_repository.save(user)

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
        return verify_password(password, user.hashed_password) 