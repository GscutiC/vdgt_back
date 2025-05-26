from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class AluminioDetalle(Base):
    __tablename__ = "aluminios_detalle"

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    codigo = Column(String)
    descripcion = Column(String)
    longitud = Column(Float)
    cantidad = Column(Integer)
    proyecto = relationship("Proyecto", backref="aluminios")
