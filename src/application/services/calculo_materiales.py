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
        return valor if unidad == "cm" else valor / 10  # convierte mm a cm

    def calcular(self):
        if self.proyecto.tipo == "ventana corrediza":
            return self._calcular_ventana_corrediza()
        else:
            raise ValueError(f"Tipo de proyecto no soportado: {self.proyecto.tipo}")

    def _calcular_ventana_corrediza(self):
        # Medidas ejemplo para vidrio y aluminio
        ancho_hoja = (self.ancho - 0.5) / 4
        alto_hoja = self.alto - 1.0
        area_vidrio = (ancho_hoja * alto_hoja) / 900  # pies cuadrados

        cantidad_vidrios = self.unidades * 2
        vidrio = VidrioDetalle(
            proyecto_id=self.proyecto.id,
            descripcion="Vidrio corredizo",
            ancho=ancho_hoja,
            alto=alto_hoja,
            cantidad=cantidad_vidrios,
            area=round(area_vidrio * cantidad_vidrios, 2)
        )
        self.db.add(vidrio)

        cantidad_perfiles = self.unidades * 2
        aluminio = AluminioDetalle(
            proyecto_id=self.proyecto.id,
            codigo="5221",
            descripcion="Perfil vertical",
            longitud=alto_hoja,
            cantidad=cantidad_perfiles
        )
        self.db.add(aluminio)

        self.db.commit()

        # Devuelve los datos como diccionario para el JSON del controlador
        return [
            {
                "descripcion": vidrio.descripcion,
                "ancho": vidrio.ancho,
                "alto": vidrio.alto,
                "cantidad": vidrio.cantidad,
                "area_total": vidrio.area
            }
        ], [
            {
                "codigo": aluminio.codigo,
                "descripcion": aluminio.descripcion,
                "longitud": aluminio.longitud,
                "cantidad": aluminio.cantidad
            }
        ]
