from flask import Blueprint, jsonify
from app.controllers.img_controller import imgController

main = Blueprint('main', __name__)
img_controller = imgController()

@main.route('/img/archivo/<path:filename>', methods=['GET'])
def ver_imagen(filename):
    return img_controller.ver_imagen(filename)

@main.route('/img/producto/<int:id>', methods=['GET'])
def imagenes_producto(id):
    return img_controller.imagenes_producto(id)