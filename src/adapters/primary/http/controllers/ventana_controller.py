from flask import Blueprint, request, jsonify
from src.infrastructure.database import get_db
from src.adapters.secondary.persistence.models.ventana_model import Ventana

ventana_blueprint = Blueprint('ventana', __name__)

@ventana_blueprint.route('/ventanas', methods=['POST'])
def crear_ventana():
    db = next(get_db())
    data = request.json
    nueva_ventana = Ventana(
        nombre=data['nombre'],
        ancho_cm=data['ancho_cm'],
        alto_cm=data['alto_cm'],
        descripcion=data.get('descripcion', '')
    )
    db.add(nueva_ventana)
    db.commit()
    return jsonify({'message': 'Ventana creada correctamente', 'id': nueva_ventana.id}), 201
