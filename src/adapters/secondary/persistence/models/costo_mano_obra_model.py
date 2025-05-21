from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class CostoManoObra(Base):
    __tablename__ = "costos_mano_obra"

    id = Column(Integer, primary_key=True, index=True)
    ventana_id = Column(Integer, ForeignKey("ventanas.id"))
    descripcion = Column(String, nullable=False)
    costo = Column(Float, nullable=False)

    ventana = relationship("Ventana", backref="costos_mano_obra")

    def __repr__(self):
        return f"<CostoManoObra(ventana_id={self.ventana_id}, costo={self.costo})>"
