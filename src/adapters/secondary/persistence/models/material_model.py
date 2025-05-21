from sqlalchemy import Column, Integer, String, Float
from src.infrastructure.database_base import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    unidad_medida = Column(String, nullable=False)  # Ej: metro, m2, unidad
    precio_unitario = Column(Float, nullable=False)
    tipo = Column(String, nullable=False)  # Ej: vidrio, perfil, accesorio

    def __repr__(self):
        return f"<Material(nombre={self.nombre}, tipo={self.tipo})>"
