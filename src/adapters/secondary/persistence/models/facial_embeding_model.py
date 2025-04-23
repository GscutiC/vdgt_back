from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base
from src.infrastructure.pgvector import PGVector

class FacialEmbedding(Base):
    __tablename__ = 'facial_embeddings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    embedding = Column(PGVector(128))  # Ajusta según la dimensión de tus embeddings
    
    user = relationship("User", back_populates="facial_embeddings")