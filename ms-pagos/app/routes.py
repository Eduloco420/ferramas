from flask import Blueprint, jsonify
from .controllers.pago_controller import PagoController

main = Blueprint('main', __name__)
pago_controller = PagoController()

@main.route('/pago', methods=['POST'])
def ingresar_pago():
    try:
        return pago_controller.ingresar_pago()
    except Exception as e:
        return jsonify({'mensaje':'Error ingresando pago', 'error':str(e)})
    
@main.route('/pago/confirmar', methods=['POST'])
def validar_pago():
    try:
        return pago_controller.confirmar_pago()
    except Exception as e:
        return jsonify({'mensaje':'Error confirmando pago', 'error':str(e)})