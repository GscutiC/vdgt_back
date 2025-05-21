from flask import Blueprint, request, jsonify
from src.infrastructure.database import get_db
from src.adapters.secondary.persistence.models.material_model import Material

material_blueprint = Blueprint('material', __name__)

@material_blueprint.route('/materiales', methods=['POST'])
def crear_material():
    db = next(get_db())
    data = request.json
    nombre = data.get('nombre')
    precio_unitario = data.get('precio_unitario')
    unidad_medida = data.get('unidad')
    tipo=data.get('tipo')

    material = Material(nombre=nombre, precio_unitario=precio_unitario, unidad_medida=unidad_medida,tipo=tipo)
    db.add(material)
    db.commit()

    return jsonify({"message": "Material creado correctamente", "material_id": material.id})
