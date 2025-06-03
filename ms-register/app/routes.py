from flask import Blueprint, jsonify
from app.controllers.register_controller import registerController 

main = Blueprint('main', __name__)
register_controller = registerController()

@main.route('/register', methods=['POST'])
def register():
    try:
        return register_controller.crear_usuario()
    except Exception as e:
        return jsonify({'mensaje':'Error llamando al servicio', 'Error':str(e)})