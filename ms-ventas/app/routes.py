from flask import Blueprint, jsonify
from .controllers.venta_controller import VentaController

main = Blueprint('main', __name__)
venta_controller = VentaController()

@main.route('/venta', methods=['POST'])
def ingresar_venta():
    try:
        return venta_controller.agregar_venta()
    except Exception as e:
        return jsonify({'mensaje': 'Error en la creación', 'error': str(e)}), 400 
    
@main.route('/venta', methods=['GET'])
def ver_ventas():
    try:
        return venta_controller.listar_ventas()
    except Exception as e:
        return jsonify({'mensaje': 'Error obteniendo ventas', 'error': str(e)}), 400     
    
@main.route('/venta/<int:id>', methods=['GET'])
def ver_venta(id):
    try:
        return venta_controller.ver_venta(id)
    except Exception as e:
        return jsonify({'mensaje': 'Error obteniendo venta', 'error': str(e)}), 400      

@main.route('/venta/<int:id>', methods=['PUT'])
def modificar_venta(id):
    try:
        return venta_controller.modificar_venta(venta=id)
    except Exception as e:
        return jsonify({'mensaje':'error modificando datos', 'error':str(e)})