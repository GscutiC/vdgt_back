from src.application.services.face_recognit import FaceRecognitionPort
import dlib
import numpy as np


class DlibFaceRecognitionAdapter(FaceRecognitionPort):
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
        self.face_database = {}  # {user_id: embedding}

    def _get_face_embedding(self, image: bytes) -> np.ndarray:
        # Convertir imagen a formato utilizable por Dlib
        img = dlib.load_rgb_image_from_bytes(image)
        faces = self.detector(img)
        if len(faces) != 1:
            raise ValueError("Debe haber exactamente un rostro en la imagen")
        shape = self.shape_predictor(img, faces[0])
        embedding = self.face_recognizer.compute_face_descriptor(img, shape)
        return np.array(embedding)

    def register_face(self, user_id: str, image: bytes) -> bool:
        embedding = self._get_face_embedding(image)
        self.face_database[user_id] = embedding
        return True

    def authenticate_face(self, image: bytes) -> str | None:
        embedding = self._get_face_embedding(image)
        for user_id, stored_embedding in self.face_database.items():
            distance = np.linalg.norm(embedding - stored_embedding)
            if distance < 0.6:  # Umbral de tolerancia ajustable
                return user_id
        return None