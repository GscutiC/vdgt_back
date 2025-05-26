from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle

class GeneradorCotizacion:

    def __init__(self, vidrios: list[VidrioDetalle], aluminios: list[AluminioDetalle]):
        self.vidrios = vidrios
        self.aluminios = aluminios

    def generar(self):
        total_vidrio = sum((v.area * 4) for v in self.vidrios)  # 4 = $/ft2
        total_aluminio = 0

        for a in self.aluminios:
            precio_unitario = self._precio_por_codigo(a.codigo)
            total = (precio_unitario / (600 / a.longitud)) * a.cantidad
            total_aluminio += total

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
            "5221": 36, "3210": 40, "7965": 30,
            "3004": 46, "8463": 55, "9116": 40,
            "8220": 60
        }
        return precios.get(codigo, 40)

    def _otros_costos_fijos(self):
        return sum([
            2.07, 20, 1.04, 4.8, 3.6, 3, 2,
            20, 20, 35, 20
        ])  # desde el ejemplo que diste
