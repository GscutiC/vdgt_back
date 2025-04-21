from src.adapters.secondary.persistence.models.facial_embeding_model import FacialEmbedding
from src.infrastructure.database import session_factory
from src.application.services.face_recognit import FaceRecognitionPort
import dlib
import numpy as np
import cv2


class DlibFaceRecognitionAdapter(FaceRecognitionPort):
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
        self.face_database = {}  # {user_id: embedding}

    def _get_face_embedding(self, image: bytes) -> np.ndarray:
    # Convertir imagen de bytes a formato numpy

        
        # Convertir bytes a numpy array
        nparr = np.frombuffer(image, np.uint8)
        # Decodificar imagen
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Convertir de BGR a RGB (dlib usa RGB)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros con dlib
        faces = self.detector(img_rgb)
        
        if len(faces) != 1:
            raise ValueError("Debe haber exactamente un rostro en la imagen")
            
        # Obtener landmarks faciales
        shape = self.shape_predictor(img_rgb, faces[0])
        # Calcular embedding
        embedding = self.face_recognizer.compute_face_descriptor(img_rgb, shape)
        
        return np.array(embedding)
    # DlibFaceRecognitionAdapter
    def register_face(self, user_id: str, image: bytes) -> bool:
        try:
            print(f"Procesando imagen facial para usuario {user_id}")
            # Extraer vector de características faciales
            embedding = self._get_face_embedding(image)
            print(f"Embedding extraído correctamente, dimensión: {len(embedding)}")
            
            # Crear instancia de FacialEmbedding y guardarla
            session = session_factory()
            try:
                embedding_list = embedding.tolist()
                facial_embedding = FacialEmbedding(
                    user_id=int(user_id),
                    embedding=embedding_list  # Convertir numpy array a lista para guardar
                )
                session.add(facial_embedding)
                session.commit()
                print(f"Embedding facial guardado en BD para usuario {user_id}")
                return True
            except Exception as e:
                session.rollback()
                print(f"Error al guardar embedding en BD: {e}")
                raise
            finally:
                session.close()
        except Exception as e:
            print(f"Error en proceso de registro facial: {e}")
            return False
    

    def authenticate_face(self, image: bytes) -> str | None:
        embedding = self._get_face_embedding(image)
        for user_id, stored_embedding in self.face_database.items():
            distance = np.linalg.norm(embedding - stored_embedding)
            if distance < 0.6:  # Umbral de tolerancia ajustable
                return user_id
        return None
    def identify_face(self, image: bytes, threshold: float = 0.6) -> str:
        """
        Identifica a un usuario basado en su rostro.
        
        Args:
            image: Imagen en bytes del rostro a identificar
            threshold: Umbral de similitud (0-1) donde 1 es coincidencia perfecta
        
        Returns:
            ID del usuario identificado o None si no se encuentra coincidencia
        """
        try:
            print("Procesando imagen para identificación facial")
            # Extraer vector de características faciales
            query_embedding = self._get_face_embedding(image)
            print(f"Embedding extraído correctamente, dimensión: {len(query_embedding)}")
            
            # Usar SQL directo para aprovechar pgvector
            session = session_factory()
            try:
                import sqlalchemy
                from sqlalchemy import text
                
                # Convertir numpy array a lista
                embedding_list = query_embedding.tolist()
                embedding_str = str(embedding_list).replace(" ", "")
                
                # Consulta utilizando el operador de distancia coseno (<=>)
                # Menor distancia coseno = mayor similitud
                query = text("""
                    SELECT fe.user_id, u.username, 1 - (fe.embedding <=> :embedding) AS similarity
                    FROM facial_embeddings fe
                    JOIN users u ON u.id = fe.user_id
                    WHERE 1 - (fe.embedding <=> :embedding) > :threshold
                    ORDER BY similarity DESC
                    LIMIT 1
                """)
                
                result = session.execute(
                    query, 
                    {"embedding": embedding_str, "threshold": threshold}
                ).fetchone()
                
                if result:
                    user_id, username, similarity = result
                    print(f"Usuario identificado: {username} (ID: {user_id}), similitud: {similarity:.4f}")
                    return str(user_id)
                else:
                    print(f"No se encontraron coincidencias por encima del umbral: {threshold}")
                    return None
                    
            except Exception as e:
                print(f"Error en la consulta de identificación: {e}")
                import traceback
                print(traceback.format_exc())
                return None
            finally:
                session.close()
        except Exception as e:
            print(f"Error en proceso de identificación facial: {e}")
            import traceback
            print(traceback.format_exc())
            return None