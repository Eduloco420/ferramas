from flask import Blueprint
from .controllers.producto_controller import ProductoController

main = Blueprint('main', __name__)
producto_controller = ProductoController()

@main.route('/productos', methods=['GET'])
def productos():
    return producto_controller.listar_productos()

@main.route('/productos', methods=['POST'])
def agregar_producto():
    return producto_controller.agregar_producto()
