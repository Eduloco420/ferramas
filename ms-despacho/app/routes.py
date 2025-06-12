from flask import Blueprint, jsonify
from .controllers.despacho_controller import DespachoController

main = Blueprint('main', __name__)
despacho_controller = DespachoController()

@main.route('/despacho', methods=['GET'])
def ver_despachos():
    try:
        return despacho_controller.listar_despachos()
    except Exception as e:
        return jsonify({'Mensaje': 'Error listando despachos', 'Error':str(e)}), 400
    
@main.route('/despacho/<int:id>', methods=['GET'])
def ver_despacho(id):
    try:
        return despacho_controller.ver_despacho(id)
    except Exception as e:
        return jsonify({'Mensaje': 'Error listando despachos', 'Error':str(e)}), 400    
    
@main.route('/despacho', methods=['POST'])
def ingresar_despacho():
    try:
        return despacho_controller.ingresar_despacho()
    except Exception as e:
        return jsonify({'mensaje':'Error ingresando despacho', 'Error':str(e)}), 400 