from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class Proyecto(Base):
    __tablename__ = 'proyectos'

    id = Column(Integer, primary_key=True)
    tipo_proyecto = Column(String, nullable=False) 
    cantidad_unidades = Column(Integer, nullable=False)
    ancho = Column(Float, nullable=False)
    alto = Column(Float, nullable=False)
    unidad_medida = Column(String, nullable=False)  
    tipo_vidrio = Column(String, nullable=False)    
    tipo_aluminio = Column(String, nullable=False)  

    # Relación uno a uno con Cotización
    cotizacion = relationship("Cotizacion", back_populates="proyecto", uselist=False)
