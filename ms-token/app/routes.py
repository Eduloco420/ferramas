from flask import Blueprint, jsonify
from .controllers.token_controller import tokenController

main = Blueprint('main', __name__)
token_controller = tokenController()

@main.route('/token/generar', methods=['POST'])
def generar():
    try:
        return token_controller.generar_token()
    except Exception as e:
        return jsonify({'mensaje':'Ha ocurrido un error durante la generación del token','Error':str(e)})

@main.route('/token/validar', methods=['POST'])
def validar():
    try:
        return token_controller.validar_token()
    except Exception as e:
        return jsonify({'mensaje':'Ha ocurrido un error durante la validación del token','Error':str(e)})
