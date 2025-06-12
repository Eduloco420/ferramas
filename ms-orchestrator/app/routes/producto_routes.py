from flask import Blueprint
from app.controllers.orchestrator_controller import OrchestratorController

producto_bp = Blueprint('producto_bp', __name__)
orchestrator_controller = OrchestratorController()

@producto_bp.route('/crear', methods=['POST'])
def crear_producto():
    return orchestrator_controller.crear_producto()

@producto_bp.route('/obtener', methods=['GET'])
def obtener_productos():
    return orchestrator_controller.obtener_productos()

@producto_bp.route('/obtener/<int:id>', methods=['GET'])
def obtener_producto(id):
    return orchestrator_controller.obtener_producto(id)

@producto_bp.route('/modificar/<int:id>', methods=['PUT'])
def modificar_producto(id):
    return orchestrator_controller.modificar_producto(id)

