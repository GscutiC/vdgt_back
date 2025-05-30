from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class VidrioDetalle(Base):
    __tablename__ = "vidrios_detalle"

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"))
    descripcion = Column(String)
    ancho = Column(Float)
    alto = Column(Float)
    cantidad = Column(Integer)
    area = Column(Float)
    proyecto = relationship("Proyecto", backref="vidrios")


    def to_dict(self):
        return {
            "id": self.id,
            "proyecto_id": self.proyecto_id,
            "descripcion": self.descripcion,
            "ancho": self.ancho,
            "alto": self.alto,
            "cantidad": self.cantidad,
            "area": self.area
        }
