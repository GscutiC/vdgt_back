from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class Material(Base):
    __tablename__ = 'materiales'

    id = Column(Integer, primary_key=True)
    cotizacion_id = Column(Integer, ForeignKey('cotizaciones.id'), nullable=False)
    descripcion = Column(String, nullable=False)      
    ancho = Column(Float, nullable=False)
    alto = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    area = Column(Float)

    # Relación con Cotización
    cotizacion = relationship("Cotizacion", back_populates="materiales")
