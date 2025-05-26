from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class CorteOptimizado(Base):
    __tablename__ = "optimizaciones"

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    descripcion = Column(String)
    datos = Column(String)  # JSON con cortes optimizados
    proyecto = relationship("Proyecto", backref="optimizaciones")
