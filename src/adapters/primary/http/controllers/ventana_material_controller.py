from flask import Blueprint, request, jsonify
from src.infrastructure.database import get_db
from src.adapters.secondary.persistence.models.ventana_material_model import VentanaMaterial
from src.adapters.secondary.persistence.models.material_model import Material

ventana_material_blueprint = Blueprint('ventana_material', __name__)

@ventana_material_blueprint.route('/ventanas/<int:ventana_id>/materiales', methods=['POST'])
def agregar_material_a_ventana(ventana_id):
    db = next(get_db())
    data = request.json
    material = db.query(Material).get(data['material_id'])

    if not material:
        return jsonify({'error': 'Material no encontrado'}), 404

    cantidad = data['cantidad']
    desperdicio = data.get('desperdicio', 0.0)
    subtotal = cantidad * material.precio_unitario

    vm = VentanaMaterial(
        ventana_id=ventana_id,
        material_id=material.id,
        cantidad=cantidad,
        desperdicio=desperdicio,
        subtotal=subtotal
    )
    db.add(vm)
    db.commit()
    return jsonify({'message': 'Material agregado a la ventana correctamente'}), 201
