from flask import Blueprint
from app.controllers.orchestrator_controller import OrchestratorController

venta_bp = Blueprint('venta_bp', __name__)
orchestrator_controller = OrchestratorController()

@venta_bp.route('/ingresar', methods=['POST'])
def ingresar_venta():
    return orchestrator_controller.ingresar_venta()

@venta_bp.route('/obtener', methods=['GET'])
def obtener_ventas():
    return orchestrator_controller.obtener_ventas()

@venta_bp.route('/obtener/<int:id>', methods=['GET'])
def obtener_venta(id):
    venta = orchestrator_controller.obtener_venta(id)
    print(venta)
    return venta

@venta_bp.route('/pago/confirmar', methods=['POST'])
def confirmar_pago():
    return orchestrator_controller.confirmar_pago()

"""@venta_bp.route('/estado', methods=['POST'])
def cambiar_estado():
    """