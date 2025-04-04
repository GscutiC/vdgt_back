from src.domain.models import User

def create_user(data):
    """Service to create a new user."""
    user = User(
        username=data.get("username"),
        email=data.get("email"),
        facial_id=data.get("facial_id"),
    )
    # Here you would save the user to the database
    return user