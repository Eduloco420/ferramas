from flask import Blueprint, jsonify
from .controllers.producto_controller import ProductoController

main = Blueprint('main', __name__)
producto_controller = ProductoController()

@main.route('/productos', methods=['GET'])
def productos():
    try:
        return producto_controller.listar_productos()
    except Exception as e:
        return jsonify({'mensaje':'Error obteniendo los datos','error':str(e)})

@main.route('/productos/<int:id>', methods=['GET'])
def producto(id):
    try:
        return producto_controller.listar_producto(id)
    except Exception as e:
        return jsonify({'mensaje':'Error obteniendo los datos', 'Error': str(e)})        

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

@main.route('/productos/precio/<int:id>', methods=['GET'])
def precio_productos(id):
    try:
        return producto_controller.ver_precio(id)
    except Exception as e:
        return jsonify({'mensaje':'Error obteniendo los datos', 'error':str(e)}), 400