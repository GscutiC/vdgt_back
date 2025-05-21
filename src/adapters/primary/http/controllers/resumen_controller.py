from flask import Blueprint, request, jsonify
from src.infrastructure.database import get_db
from src.adapters.secondary.persistence.models.resumen_costo_model import ResumenCosto
from src.adapters.secondary.persistence.models.ventana_model import Ventana
from src.adapters.secondary.persistence.models.ventana_material_model import VentanaMaterial
from src.adapters.secondary.persistence.models.material_model import Material
from src.adapters.secondary.persistence.models.costo_mano_obra_model import CostoManoObra

resumen_blueprint = Blueprint('resumen', __name__)

@resumen_blueprint.route('/resumen/calcular', methods=['POST'])
def calcular_resumen():
    db = next(get_db())
    data = request.get_json()
    ventana_id = data.get('ventana_id')

    if not ventana_id:
        return jsonify({"error": "Se requiere el ID de la ventana"}), 400

    # Obtener la ventana
    ventana = db.query(Ventana).filter_by(id=ventana_id).first()
    if not ventana:
        return jsonify({"error": "Ventana no encontrada"}), 404

    # Obtener materiales usados en esta ventana
    ventana_materiales = db.query(VentanaMaterial).filter_by(ventana_id=ventana_id).all()

    total_materiales = 0
    for vm in ventana_materiales:
        material = db.query(Material).filter_by(id=vm.material_id).first()
        if material:
            total_materiales += vm.cantidad * material.precio_unitario

    # Obtener mano de obra asociada a esta ventana
    mano_obras = db.query(CostoManoObra).filter_by(ventana_id=ventana_id).all()
    total_mano_obra = sum(mo.costo for mo in mano_obras)

    # Cálculo total
    total_general = total_materiales + total_mano_obra

    # Guardar resumen en la base de datos
    resumen_existente = db.query(ResumenCosto).filter_by(ventana_id=ventana_id).first()
    if resumen_existente:
        # Actualiza si ya existe
        resumen_existente.costo_total_materiales = total_materiales
        resumen_existente.costo_total_mano_obra = total_mano_obra
        resumen_existente.costo_final = total_general
    else:
        resumen = ResumenCosto(
            ventana_id=ventana_id,
            total_materiales=total_materiales,
            total_mano_obra=total_mano_obra,
            total_general=total_general
        )
        db.add(resumen)

    db.commit()

    return jsonify({
        "ventana_id": ventana_id,
        "costo total_materiales": total_materiales,
        "costo total_mano_obra": total_mano_obra,
        "costo_general": total_general
    }), 200
