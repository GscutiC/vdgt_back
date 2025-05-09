from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class Cotizacion(Base):
    __tablename__ = 'cotizaciones'

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey('proyectos.id'), nullable=False)
    area_total_vidrio = Column(Float)
    porcentaje_desperdicio = Column(Float)

    # Relación con Proyecto
    proyecto = relationship("Proyecto", back_populates="cotizacion")

    # Relación con Materiales
    materiales = relationship("Material", back_populates="cotizacion")
