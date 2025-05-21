from sqlalchemy import Column, Integer, String, Float, Text
from src.infrastructure.database_base import Base

class Ventana(Base):
    __tablename__ = "ventanas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ancho_cm = Column(Float, nullable=False)
    alto_cm = Column(Float, nullable=False)
    descripcion = Column(Text)

    def __repr__(self):
        return f"<Ventana(nombre={self.nombre}, ancho={self.ancho_cm}, alto={self.alto_cm})>"
