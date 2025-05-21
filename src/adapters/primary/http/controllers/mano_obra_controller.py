from flask import Blueprint, request, jsonify
from src.infrastructure.database import get_db
from src.adapters.secondary.persistence.models.costo_mano_obra_model import CostoManoObra

mano_obra_blueprint = Blueprint('mano_obra_', __name__)

@mano_obra_blueprint.route('/ventanas/<int:ventana_id>/mano_obra', methods=['POST'])
def agregar_mano_obra(ventana_id):
    db = next(get_db())
    data = request.json
    nueva_mano_obra = CostoManoObra(
        ventana_id=ventana_id,
        descripcion=data['descripcion'],
        costo=data['costo']
    )
    db.add(nueva_mano_obra)
    db.commit()
    return jsonify({'message': 'Costo de mano de obra agregado'}), 201
