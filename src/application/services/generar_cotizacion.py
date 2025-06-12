from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle

LONGITUD_BARRA = 600  # cm

PRECIOS_VIDRIO = {
    "vidrio templado de 6mm": 5.5,
    "vidrio templado de 8mm": 6.5,
    "vidrio laminado 6mm": 7.0,
    "doble acristalamiento 18mm": 8.5,
}

PRECIOS_ALUMINIO = {
    "aluminio schuco 50": 60,
    "aluminio exlabesa serie 500": 55,
    "aluminio technal frente plano": 58,
    "aluminio cortizo 4200": 62,
}

class GeneradorCotizacion:

    def __init__(self, vidrios: list[VidrioDetalle], aluminios: list[AluminioDetalle]):
        self.vidrios = vidrios
        self.aluminios = aluminios

    def generar(self):
        total_vidrio = sum(
            (v.area * self._precio_vidrio(v.tipo)) for v in self.vidrios
        )

        total_aluminio = 0
        for a in self.aluminios:
            precio_barra = self._precio_aluminio(a.tipo)
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

    def _precio_vidrio(self, tipo):
        return PRECIOS_VIDRIO.get(tipo.lower(), 6.0)

    def _precio_aluminio(self, tipo):
        return PRECIOS_ALUMINIO.get(tipo.lower(), 55)

    def _otros_costos_fijos(self):
        return sum([
            2.07, 20, 1.04, 4.8, 3.6, 3, 2, 20, 20, 35, 20
        ])
