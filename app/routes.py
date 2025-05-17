from flask import Blueprint, jsonify
from .controllers.producto_controller import ProductoController
from .controllers.venta_controller import VentaController

main = Blueprint('main', __name__)
producto_controller = ProductoController()
venta_controller = VentaController()

@main.route('/productos', methods=['GET'])
def productos():
    try:
        return producto_controller.listar_productos()
    except Exception as e:
        return jsonify({'mensaje':'Error obteniendo los datos','error':str(e)})

@main.route('/productos', methods=['POST'])
def agregar_producto():
    try:
        return producto_controller.agregar_producto()
    except Exception as e:
        return jsonify({'mensaje': 'Error en la creación', 'error': str(e)}), 400

@main.route('/productos/<int:id>', methods=['PUT'])
def modificar_producto(id):
    try:
        return producto_controller.modificar_producto(id)
    except Exception as e:
        return jsonify({'mensaje':'Error modificando los datos'}), 400
    
@main.route('/venta', methods=['POST'])
def ingresar_venta():
    try:
        return venta_controller.agregar_venta()
    except Exception as e:
        return jsonify({'mensaje': 'Error en la creación', 'error': str(e)}), 400 