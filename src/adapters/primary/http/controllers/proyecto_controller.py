from flask import Blueprint, jsonify, request
from src.adapters.secondary.persistence.models.proyecto_model import Proyecto
from src.adapters.secondary.persistence.models.vidrio_model import VidrioDetalle
from src.adapters.secondary.persistence.models.aluminio_model import AluminioDetalle
from src.adapters.secondary.persistence.models.optimizacion_model import CorteOptimizado
from src.adapters.secondary.persistence.models.cotizacion_model import Cotizacion 
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
def obtener_materiales(proyecto_id):
    db = db_session()
    proyecto = db.query(Proyecto).get(proyecto_id)

    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    calculadora = CalculadoraMateriales(db, proyecto)
    vidrios, aluminios = calculadora.calcular()

    return jsonify({
        "vidrios": [{
            "id": v.id,
            "proyecto_id": v.proyecto_id,
            "descripcion": v.descripcion,
            "ancho": v.ancho,
            "alto": v.alto,
            "cantidad": v.cantidad,
            "area": v.area
        } for v in vidrios],
        "aluminios": [{
            "id": a.id,
            "proyecto_id": a.proyecto_id,
            "codigo": a.codigo,
            "descripcion": a.descripcion,
            "longitud": a.longitud,
            "cantidad": a.cantidad
        } for a in aluminios]
    })



@proyecto_blueprint.route('/proyectos/<int:proyecto_id>/optimizacion', methods=['GET'])
def obtener_optimizacion(proyecto_id):
    db = db_session()
    proyecto = db.query(Proyecto).get(proyecto_id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    try:
        aluminios = db.query(AluminioDetalle).filter_by(proyecto_id=proyecto.id).all()
        optimizador = OptimizadorCortes(aluminios)
        cortes = optimizador.optimizar()

        # Guardar la optimización en base de datos
        import json
        optimizacion_json = json.dumps(cortes)

        optimizacion_db = CorteOptimizado(
            proyecto_id=proyecto.id,
            descripcion=f"Optimización cortes proyecto {proyecto.id}",
            datos=optimizacion_json
        )
        db.add(optimizacion_db)
        db.commit()

        return jsonify({"optimizacion_cortes": cortes})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@proyecto_blueprint.route('/proyectos/<int:proyecto_id>/cotizacion', methods=['GET'])
def obtener_cotizacion(proyecto_id):
    db = db_session()
    proyecto = db.query(Proyecto).get(proyecto_id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404

    try:
        vidrios = db.query(VidrioDetalle).filter_by(proyecto_id=proyecto.id).all()
        aluminios = db.query(AluminioDetalle).filter_by(proyecto_id=proyecto.id).all()

        generador = GeneradorCotizacion(vidrios, aluminios)
        cotizacion = generador.generar()

        # Guardar cotización en la base de datos
        cotizacion_db = Cotizacion(
            proyecto_id=proyecto.id,
            subtotal=cotizacion["subtotal"],
            iva=cotizacion["iva"],
            total=cotizacion["total"]
        )
        db.add(cotizacion_db)
        db.commit()

        return jsonify(cotizacion)
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500