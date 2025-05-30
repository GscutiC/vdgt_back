from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    subtotal = Column(Float)
    iva = Column(Float)
    total = Column(Float)
    proyecto = relationship("Proyecto", backref="cotizacion")
