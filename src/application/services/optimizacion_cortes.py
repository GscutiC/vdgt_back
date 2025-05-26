from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle

LONGITUD_BARRA = 600  # cm

class OptimizadorCortes:

    def __init__(self, aluminio_detalles: list[AluminioDetalle]):
        self.detalles = aluminio_detalles

    def optimizar(self):
        cortes = []

        for detalle in self.detalles:
            longitud_necesaria = detalle.longitud
            cantidad = detalle.cantidad
            for _ in range(cantidad):
                colocado = False
                for barra in cortes:
                    sobrante = LONGITUD_BARRA - sum(barra)
                    if sobrante >= longitud_necesaria:
                        barra.append(longitud_necesaria)
                        colocado = True
                        break
                if not colocado:
                    cortes.append([longitud_necesaria])

        return cortes  # lista de listas, cada sublista es una barra con los cortes
