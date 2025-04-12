from typing import List, Optional
from src.domain.entities.user import User
from src.domain.services.user_service import UserService

class UserManagementUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, username: str, email: str, password: str, full_name: str) -> User:
        return self.user_service.create_user(username, email, password, full_name)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_service.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_service.get_user_by_email(email)

    def list_all_users(self) -> List[User]:
        return self.user_service.list_all_users()

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        return self.user_service.update_user(user_id, **kwargs)

    def delete_user(self, user_id: int) -> bool:
        return self.user_service.delete_user(user_id)
