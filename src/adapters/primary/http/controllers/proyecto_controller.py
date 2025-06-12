from flask import Blueprint, jsonify, request
from src.adapters.secondary.persistence.models.proyecto_model import Proyecto
from src.infrastructure.database import db_session
from src.application.services.servicio_proyecto import ServicioProyecto

proyecto_blueprint = Blueprint('proyecto', __name__)

@proyecto_blueprint.route('/proyectos', methods=['POST'])
def crear_proyecto():
    data = request.json

    TIPOS_PROYECTO_VALIDOS = [
        "ventana corrediza", "puerta plegable", "puerta batiente", "ventana fija"
    ]
    TIPOS_VIDRIO_VALIDOS = [
        "vidrio templado de 6mm", "vidrio templado de 8mm",
        "vidrio laminado de 6mm", "doble acristalamiento de 18mm"
    ]
    TIPOS_ALUMINIO_VALIDOS = [
        "aluminio schuco 50", "aluminio exlabesa serie 500",
        "aluminio technal frente plano", "aluminio cortizo 4200"
    ]

    errores = []
    if data['tipo'] not in TIPOS_PROYECTO_VALIDOS:
        errores.append(f"Tipo de proyecto inválido: '{data['tipo']}'")
    if data['tipo_vidrio'] not in TIPOS_VIDRIO_VALIDOS:
        errores.append(f"Tipo de vidrio inválido: '{data['tipo_vidrio']}'")
    if data['tipo_aluminio'] not in TIPOS_ALUMINIO_VALIDOS:
        errores.append(f"Tipo de aluminio inválido: '{data['tipo_aluminio']}'")

    if errores:
        return jsonify({"error": "Datos inválidos", "detalles": errores}), 400

    try:
        nuevo = Proyecto(
            tipo=data['tipo'],
            unidades=data['unidades'],
            ancho=data['ancho'],
            alto=data['alto'],
            unidad_medida=data['unidad_medida'],
            tipo_vidrio=data['tipo_vidrio'],
            tipo_aluminio=data['tipo_aluminio']
        )
        db = db_session()
        db.add(nuevo)
        db.commit()
        return jsonify({"mensaje": "Proyecto creado", "proyecto_id": nuevo.id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400


@proyecto_blueprint.route('/proyectos/<int:id>/materiales', methods=['GET'])
def ver_materiales(id):
    db = db_session()
    proyecto = db.query(Proyecto).get(id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    servicio = ServicioProyecto(db)
    vidrios, aluminios = servicio.calcular_materiales(proyecto)
    return jsonify({
        "vidrios": [v.to_dict() for v in vidrios],
        "aluminios": [a.to_dict() for a in aluminios]
    })

@proyecto_blueprint.route('/proyectos/<int:id>/materiales', methods=['POST'])
def guardar_materiales(id):
    db = db_session()
    proyecto = db.query(Proyecto).get(id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    servicio = ServicioProyecto(db)
    vidrios, aluminios = servicio.guardar_materiales(proyecto)
    return jsonify({"mensaje": "Materiales guardados correctamente"})

@proyecto_blueprint.route('/proyectos/<int:id>/optimizacion', methods=['GET'])
def ver_optimizacion(id):
    db = db_session()
    proyecto = db.query(Proyecto).get(id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    servicio = ServicioProyecto(db)
    datos = servicio.calcular_optimizacion(proyecto)
    return jsonify(datos)

@proyecto_blueprint.route('/proyectos/<int:id>/optimizacion', methods=['POST'])
def guardar_optimizacion(id):
    db = db_session()
    proyecto = db.query(Proyecto).get(id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    servicio = ServicioProyecto(db)
    datos = servicio.guardar_optimizacion(proyecto)
    return jsonify({"mensaje": "Optimización guardada", "optimizacion": datos})

@proyecto_blueprint.route('/proyectos/<int:id>/cotizacion', methods=['GET'])
def ver_cotizacion(id):
    db = db_session()
    proyecto = db.query(Proyecto).get(id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    servicio = ServicioProyecto(db)
    cotizacion = servicio.calcular_cotizacion(proyecto)
    return jsonify(cotizacion)

@proyecto_blueprint.route('/proyectos/<int:id>/cotizacion', methods=['POST'])
def guardar_cotizacion(id):
    db = db_session()
    proyecto = db.query(Proyecto).get(id)
    if not proyecto:
        return jsonify({"error": "Proyecto no encontrado"}), 404
    servicio = ServicioProyecto(db)
    cotizacion = servicio.guardar_cotizacion(proyecto)
    return jsonify({"mensaje": "Cotización guardada", "cotizacion": cotizacion})