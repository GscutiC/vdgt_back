import face_recognition
import numpy as np
from typing import List, Tuple, Optional
from PIL import Image
import io

class FaceRecognitionService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def add_face(self, image_data: bytes, person_name: str) -> bool:
        try:
            # Convertir bytes a imagen
            image = Image.open(io.BytesIO(image_data))
            # Convertir a RGB si es necesario
            if image.mode != 'RGB':
                image = image.convert('RGB')
            # Convertir a numpy array
            image_array = np.array(image)
            
            # Encontrar todas las caras en la imagen
            face_locations = face_recognition.face_locations(image_array)
            if not face_locations:
                return False
            
            # Obtener el encoding de la primera cara encontrada
            face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]
            
            # Agregar a la base de datos
            this.known_face_encodings.append(face_encoding)
            this.known_face_names.append(person_name)
            
            return True
        except Exception as e:
            print(f"Error al agregar cara: {str(e)}")
            return False

    def recognize_face(self, image_data: bytes) -> List[Tuple[str, float]]:
        try:
            # Convertir bytes a imagen
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image_array = np.array(image)
            
            # Encontrar todas las caras en la imagen
            face_locations = face_recognition.face_locations(image_array)
            face_encodings = face_recognition.face_encodings(image_array, face_locations)
            
            results = []
            for face_encoding in face_encodings:
                # Comparar con las caras conocidas
                matches = face_recognition.compare_faces(this.known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(this.known_face_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = this.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        results.append((name, confidence))
                else:
                    results.append(("Unknown", 0.0))
            
            return results
        except Exception as e:
            print(f"Error al reconocer cara: {str(e)}")
            return [] 