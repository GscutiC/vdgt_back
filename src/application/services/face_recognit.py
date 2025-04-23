from abc import ABC, abstractmethod

class FaceRecognitionPort(ABC):
    @abstractmethod
    def register_face(self, user_id: str, image: bytes) -> bool:
        """Registra las características faciales de un usuario."""
        pass

    @abstractmethod
    def authenticate_face(self, image: bytes) -> str | None:
        """Autentica un rostro y devuelve el user_id si coincide."""
        pass