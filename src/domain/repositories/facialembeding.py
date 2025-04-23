from typing import Optional, List
from sqlalchemy import text
import numpy as np
from src.infrastructure.database import session_factory
from adapters.secondary.persistence.models.facial_embeding_model import FacialEmbedding
from src.adapters.secondary.persistence.models.user_model import User

class FacialEmbeddingRepository:
    def __init__(self):
        pass
    
    def save_embedding(self, user_id: int, embedding: np.ndarray) -> FacialEmbedding:
        """Guarda un embedding facial para un usuario"""
        session = session_factory()
        try:
            facial_embedding = FacialEmbedding(user_id=user_id, embedding=embedding)
            session.add(facial_embedding)
            session.commit()
            session.refresh(facial_embedding)
            return facial_embedding
        except Exception as e:
            session.rollback()
            print(f"Error guardando embedding facial: {e}")
            raise
        finally:
            session.close()
    
    def find_most_similar(self, embedding: np.ndarray, threshold: float = 0.75) -> Optional[User]:
        """
        Encuentra el usuario más similar basado en el embedding facial.
        Utiliza la función de coseno de similitud de pgvector.
        
        :param embedding: Vector de características faciales
        :param threshold: Umbral de similitud mínimo (0-1)
        :return: Usuario encontrado o None
        """
        session = session_factory()
        try:
            # Convertir embedding a formato compatible con pgvector
            embedding_str = str(embedding.tolist())
            
            # Consulta con SQL nativo para usar pgvector
            query = text("""
                SELECT u.*, 
                       1 - (fe.embedding <=> :embedding) as similarity
                FROM facial_embeddings fe
                JOIN users u ON fe.user_id = u.id
                WHERE 1 - (fe.embedding <=> :embedding) > :threshold
                ORDER BY similarity DESC
                LIMIT 1
            """)
            
            result = session.execute(
                query, 
                {"embedding": embedding_str, "threshold": threshold}
            ).fetchone()
            
            if result:
                user = session.query(User).get(result.id)
                return user
            return None
        finally:
            session.close()