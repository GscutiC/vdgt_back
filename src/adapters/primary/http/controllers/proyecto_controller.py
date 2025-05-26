from flask import Blueprint, jsonify, request
from src.adapters.secondary.persistence.models.proyecto_model import Proyecto
from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle
from src.application.services.calculo_materiales import CalculadoraMateriales
from src.application.services.optimizacion_cortes import OptimizadorCortes
from src.application.services.generar_cotizacion import GeneradorCotizacion
from src.infrastructure.database import db_session

proyecto_blueprint = Blueprint('proyecto', __name__)

@proyecto_blueprint.route('/proyectos', methods=['POST'])
def crear_proyecto():
    data = request.json

    try:
        nuevo_proyecto = Proyecto(
            tipo=data['tipo'],
            unidades=data['unidades'],
            ancho=data['ancho'],
            alto=data['alto'],
            unidad_medida=data['unidad_medida'],
            tipo_vidrio=data['tipo_vidrio'],
            tipo_aluminio=data['tipo_aluminio'],
            
        )
        db_session.add(nuevo_proyecto)
        db_session.commit()

        return jsonify({"mensaje": "Proyecto creado", "proyecto_id": nuevo_proyecto.id}), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 400

@proyecto_blueprint.route('/proyectos/<int:proyecto_id>/materiales', methods=['GET'])
def calcular_materiales(proyecto_id):
    proyecto = db_session.query(Proyecto).get(proyecto_id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    calculador = CalculadoraMateriales(proyecto)
    detalles_vidrio, detalles_aluminio = calculador.calcular()

    optimizador = OptimizadorCortes(detalles_aluminio)
    cortes = optimizador.optimizar()

    return jsonify({
        "vidrio": [
            {
                "descripcion": v.descripcion,
                "ancho": v.ancho,
                "alto": v.alto,
                "area": round(v.area, 2),
                "cantidad": v.cantidad
            } for v in detalles_vidrio
        ],
        "aluminio": [
            {
                "codigo": a.codigo,
                "descripcion": a.descripcion,
                "longitud": a.longitud,
                "cantidad": a.cantidad
            } for a in detalles_aluminio
        ],
        "optimizacion": cortes  # Lista de cortes por barra
    })

@proyecto_blueprint.route('/proyectos/<int:proyecto_id>/cotizacion', methods=['GET'])
def generar_cotizacion(proyecto_id):
    proyecto = db_session.query(Proyecto).get(proyecto_id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    calculador = CalculadoraMateriales(proyecto)
    vidrios, aluminios = calculador.calcular()

    generador = GeneradorCotizacion(vidrios, aluminios)
    cotizacion = generador.generar()

    return jsonify(cotizacion)
