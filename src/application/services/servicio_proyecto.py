from src.application.services.calculo_materiales import CalculadoraMateriales
from src.application.services.optimizacion_cortes import OptimizadorCortes
from src.application.services.generar_cotizacion import GeneradorCotizacion
from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle
from src.adapters.secondary.persistence.models.optimizacion_model import CorteOptimizado
from src.adapters.secondary.persistence.models.cotizacion_model import Cotizacion
from sqlalchemy.orm import Session
import json

class ServicioProyecto:

    def __init__(self, db: Session):
        self.db = db

    def calcular_materiales(self, proyecto):
        calculadora = CalculadoraMateriales(self.db, proyecto)
        return calculadora.calcular()

    def guardar_materiales(self, proyecto):
        # eliminar materiales previos
        self.db.query(VidrioDetalle).filter_by(proyecto_id=proyecto.id).delete()
        self.db.query(AluminioDetalle).filter_by(proyecto_id=proyecto.id).delete()
        self.db.commit()  # para aplicar borrado

        vidrios, aluminios = self.calcular_materiales(proyecto)
        self.db.add_all(vidrios + aluminios)
        self.db.commit()
        return vidrios, aluminios

    def calcular_optimizacion(self, proyecto):
        aluminios = self.db.query(AluminioDetalle).filter_by(proyecto_id=proyecto.id).all()
        optimizador = OptimizadorCortes(aluminios)
        return optimizador.optimizar()

    def guardar_optimizacion(self, proyecto):
        # eliminar optimizacion previos
        datos = self.calcular_optimizacion(proyecto)
        self.db.query(CorteOptimizado).filter_by(proyecto_id=proyecto.id).delete()
        self.db.commit() # para aplicar borrado

        optimizacion_db = CorteOptimizado(
            proyecto_id=proyecto.id,
            descripcion=f"Optimización cortes proyecto {proyecto.id}",
            datos=json.dumps(datos)
        )
        self.db.add(optimizacion_db)
        self.db.commit()
        return datos

    def calcular_cotizacion(self, proyecto):
        vidrios = self.db.query(VidrioDetalle).filter_by(proyecto_id=proyecto.id).all()
        aluminios = self.db.query(AluminioDetalle).filter_by(proyecto_id=proyecto.id).all()
        generador = GeneradorCotizacion(vidrios, aluminios)
        return generador.generar()

    def guardar_cotizacion(self, proyecto):
        # eliminar cotizacion previa
        self.db.query(Cotizacion).filter_by(proyecto_id=proyecto.id).delete()
        self.db.commit() # para aplicar borrado

        cotizacion = self.calcular_cotizacion(proyecto)
        cotizacion_db = Cotizacion(
            proyecto_id=proyecto.id,
            subtotal=cotizacion["subtotal"],
            iva=cotizacion["iva"],
            total=cotizacion["total"]
        )
        self.db.add(cotizacion_db)
        self.db.commit()
        return cotizacion
