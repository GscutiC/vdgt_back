from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle
from src.adapters.secondary.persistence.models.proyecto_model import Proyecto
from sqlalchemy.orm import Session

class CalculadoraMateriales:

    def __init__(self, db: Session, proyecto: Proyecto):
        self.db = db
        self.proyecto = proyecto
        self.unidades = proyecto.unidades
        self.ancho = self._convertir_a_cm(proyecto.ancho, proyecto.unidad_medida)
        self.alto = self._convertir_a_cm(proyecto.alto, proyecto.unidad_medida)

    def _convertir_a_cm(self, valor, unidad):
        return valor if unidad == "cm" else valor / 10  # mm a cm

    def calcular(self):
        if self.proyecto.tipo == "ventana corrediza":
            self._calcular_ventana_corrediza()

    def _calcular_ventana_corrediza(self):
        # Ejemplo simple con medidas de muestra
        ancho_hoja = (self.ancho - 0.5) / 4
        alto_hoja = self.alto - 1.0
        area_vidrio = (ancho_hoja * alto_hoja) / 900  # pies cuadrados

        vidrio = VidrioDetalle(
            proyecto_id=self.proyecto.id,
            descripcion="Vidrio corredizo",
            ancho=ancho_hoja,
            alto=alto_hoja,
            cantidad=self.unidades * 2,  # 2 hojas
            area=round(area_vidrio, 2)
        )
        self.db.add(vidrio)

        aluminio = AluminioDetalle(
            proyecto_id=self.proyecto.id,
            codigo="5221",
            descripcion="Perfil vertical",
            longitud=alto_hoja,
            cantidad=self.unidades * 2
        )
        self.db.add(aluminio)

        self.db.commit()
