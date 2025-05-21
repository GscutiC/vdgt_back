from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class ResumenCosto(Base):
    __tablename__ = "resumen_costos"

    id = Column(Integer, primary_key=True)
    ventana_id = Column(Integer, ForeignKey("ventanas.id"))
    costo_total_materiales = Column(Float)
    costo_total_mano_obra = Column(Float)
    costo_final = Column(Float)

    ventana = relationship("Ventana", backref="resumen_costo")

    def __repr__(self):
        return f"<ResumenCosto(ventana_id={self.ventana_id}, total={self.costo_final})>"
