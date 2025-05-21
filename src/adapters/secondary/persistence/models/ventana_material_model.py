from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database_base import Base

class VentanaMaterial(Base):
    __tablename__ = "ventana_materiales"

    id = Column(Integer, primary_key=True, index=True)
    ventana_id = Column(Integer, ForeignKey("ventanas.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))

    cantidad = Column(Float, nullable=False)
    desperdicio = Column(Float, default=0.0)  # Porcentaje de desperdicio
    subtotal = Column(Float, nullable=False)  # cantidad * precio_unitario

    ventana = relationship("Ventana", backref="materiales_usados")
    material = relationship("Material")

    def __repr__(self):
        return f"<VentanaMaterial(ventana_id={self.ventana_id}, material_id={self.material_id}, subtotal={self.subtotal})>"
