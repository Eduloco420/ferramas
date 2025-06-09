from flask import Blueprint, jsonify
from .controllers.mail_controller import mailController

main = Blueprint('main', __name__)
mail_controller = mailController()

@main.route('/mail', methods=['POST'])
def enviar():
    try:
        return mail_controller.enviar_correo()
    except Exception as e:
        return jsonify({'mensaje':'Error enviando correo electronico', 'Error':str(e)})