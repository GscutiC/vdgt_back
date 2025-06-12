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
    tipo = Column(String, nullable=True) 
    proyecto = relationship("Proyecto", backref="aluminios")

    def to_dict(self):
        return {
            "id": self.id,
            "proyecto_id": self.proyecto_id,
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "longitud": self.longitud,
            "cantidad": self.cantidad,
            "tipo": self.tipo
        }
