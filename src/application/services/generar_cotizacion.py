from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle

PRECIO_VIDRIO_PIE2 = 4  # dólares por pie²
LONGITUD_BARRA = 600  # cm

class GeneradorCotizacion:

    def __init__(self, vidrios: list[VidrioDetalle], aluminios: list[AluminioDetalle]):
        self.vidrios = vidrios
        self.aluminios = aluminios

    def generar(self):
        total_vidrio = sum((v.area * PRECIO_VIDRIO_PIE2) for v in self.vidrios)

        total_aluminio = 0
        for a in self.aluminios:
            precio_barra = self._precio_por_codigo(a.codigo)
            costo_por_corte = (a.longitud / LONGITUD_BARRA) * precio_barra
            total_aluminio += costo_por_corte * a.cantidad

        otros = self._otros_costos_fijos()

        subtotal = total_vidrio + total_aluminio + otros
        iva = subtotal * 0.16
        total = subtotal + iva

        return {
            "vidrios": round(total_vidrio, 2),
            "aluminio": round(total_aluminio, 2),
            "otros": round(otros, 2),
            "subtotal": round(subtotal, 2),
            "iva": round(iva, 2),
            "total": round(total, 2)
        }

    def _precio_por_codigo(self, codigo):
        precios = {
            "5221": 36,
            "3210": 40,
            "7965": 30,
            "3004": 46,
            "8463": 55,
            "9116": 40,
            "8220": 60
        }
        return precios.get(codigo, 40)

    def _otros_costos_fijos(self):
        # Puedes migrar esto luego a una tabla de "CostosFijos"
        return sum([
            2.07,  # seguro
            20,    # empaques
            1.04,  # escuadras
            4.8,   # tornillos
            3.6,   # taquetes
            3,     # brocas
            2,     # remaches
            20,    # transporte
            20,    # instalación
            35,    # mano de obra
            20     # limpieza
        ])
