from flask import Blueprint, jsonify
from .controllers.auth_controller import AuthController

main = Blueprint('main', __name__)
auth_controller = AuthController()

@main.route('/login', methods=['POST'])
def login():
    try:
        return auth_controller.login()
    except Exception as e:
        return jsonify({'mensaje':'Ha ocurrido un error durante el inicio de sesión', 'Error':str(e)}), 400

@main.route('/verify/token', methods=['GET'])
def validar_token():
    try:
        return auth_controller.validar_token()
    except Exception as e:
        return jsonify({'mensaje':'Error validando el Token', 'Error':str(e)})            