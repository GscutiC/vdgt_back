from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle

LONGITUD_BARRA = 600  # cm

class OptimizadorCortes:

    def __init__(self, aluminio_detalles: list[AluminioDetalle]):
        self.detalles = aluminio_detalles

    def optimizar(self):
        resultados = []

        # Agrupar por código de perfil
        perfiles = {}
        for detalle in self.detalles:
            if detalle.codigo not in perfiles:
                perfiles[detalle.codigo] = []
            perfiles[detalle.codigo].extend([detalle.longitud] * detalle.cantidad)

        # Optimizar cortes para cada perfil
        for codigo, cortes_requeridos in perfiles.items():
            barras = []

            for corte in cortes_requeridos:
                colocado = False
                for barra in barras:
                    sobrante = LONGITUD_BARRA - sum(barra)
                    if sobrante >= corte:
                        barra.append(corte)
                        colocado = True
                        break
                if not colocado:
                    barras.append([corte])  # nueva barra

            # Guardar resultado por código de perfil
            resultado_perfil = {
                "codigo": codigo,
                "barras_utilizadas": len(barras),
                "detalle_barras": [
                    {
                        "cortes": barra,
                        "suma_cortes": sum(barra),
                        "desperdicio": round(LONGITUD_BARRA - sum(barra), 2)
                    }
                    for barra in barras
                ]
            }
            resultados.append(resultado_perfil)

        return resultados
