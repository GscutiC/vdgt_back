from sqlalchemy import Column, Integer, String, Float, Enum
from src.infrastructure.database_base import Base

class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # Ej: "ventana corrediza"
    unidades = Column(Integer, nullable=False)
    ancho = Column(Float, nullable=False)
    alto = Column(Float, nullable=False)
    unidad_medida = Column(String, nullable=False)  # mm o cm
    tipo_vidrio = Column(String, nullable=False)
    tipo_aluminio = Column(String, nullable=False)
