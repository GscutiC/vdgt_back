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
        tipo = self.proyecto.tipo.lower()

        if tipo == "ventana corrediza":
            return self._ventana_corrediza()
        elif tipo == "ventana pegable":
            return self._ventana_pegable()
        elif tipo == "puerta batiente":
            return self._puerta_batiente()
        elif tipo == "ventana fijo":
            return self._fijo()
        else:
            raise ValueError(f"Tipo de proyecto no soportado: {self.proyecto.tipo}")

    def _ventana_corrediza(self):
        ancho_hoja = (self.ancho - 0.5) / 4
        alto_hoja = self.alto - 1.0
        area_vidrio = (ancho_hoja * alto_hoja) / 900

        vidrio = VidrioDetalle(
            proyecto_id=self.proyecto.id,
            descripcion="Vidrio corredizo",
            ancho=ancho_hoja,
            alto=alto_hoja,
            cantidad=self.unidades * 2,
            area=round(area_vidrio, 2)
        )

        aluminio = AluminioDetalle(
            proyecto_id=self.proyecto.id,
            codigo="5221",
            descripcion="Perfil vertical",
            longitud=alto_hoja,
            cantidad=self.unidades * 2
        )

        self.db.add(vidrio)
        self.db.add(aluminio)
        self.db.commit()
        return [vidrio], [aluminio]

    def _ventana_pegable(self):
        vidrio = VidrioDetalle(
            proyecto_id=self.proyecto.id,
            descripcion="Vidrio abatible",
            ancho=self.ancho - 2,
            alto=self.alto - 2,
            cantidad=self.unidades,
            area=round(((self.ancho - 2) * (self.alto - 2)) / 900, 2)
        )

        aluminio = AluminioDetalle(
            proyecto_id=self.proyecto.id,
            codigo="3210",
            descripcion="Marco abatible",
            longitud=self.ancho + self.alto,
            cantidad=self.unidades * 2
        )

        self.db.add(vidrio)
        self.db.add(aluminio)
        self.db.commit()
        return [vidrio], [aluminio]

    def _puerta_batiente(self):
        vidrio = VidrioDetalle(
            proyecto_id=self.proyecto.id,
            descripcion="Vidrio puerta",
            ancho=self.ancho - 3,
            alto=self.alto - 3,
            cantidad=self.unidades,
            area=round(((self.ancho - 3) * (self.alto - 3)) / 900, 2)
        )

        aluminio = AluminioDetalle(
            proyecto_id=self.proyecto.id,
            codigo="7965",
            descripcion="Marco puerta",
            longitud=self.ancho + self.alto,
            cantidad=self.unidades * 3
        )

        self.db.add(vidrio)
        self.db.add(aluminio)
        self.db.commit()
        return [vidrio], [aluminio]

    def _fijo(self):
        vidrio = VidrioDetalle(
            proyecto_id=self.proyecto.id,
            descripcion="Vidrio fijo",
            ancho=self.ancho,
            alto=self.alto,
            cantidad=self.unidades,
            area=round((self.ancho * self.alto) / 900, 2)
        )

        aluminio = AluminioDetalle(
            proyecto_id=self.proyecto.id,
            codigo="3004",
            descripcion="Marco fijo",
            longitud=self.ancho + self.alto,
            cantidad=self.unidades * 2
        )

        self.db.add(vidrio)
        self.db.add(aluminio)
        self.db.commit()
        return [vidrio], [aluminio]

  