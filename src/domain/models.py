class User:
    """Domain model for a User."""

    def __init__(self, username, email, facial_id):
        self.username = username
        self.email = email
        self.facial_id = facial_id

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, facial_id={self.facial_id})>"