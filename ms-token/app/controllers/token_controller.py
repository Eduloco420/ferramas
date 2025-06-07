import jwt
import datetime
from flask import request, jsonify
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')

class tokenController:
    def generar_token(self):
        data = request.get_json()
        mail = data['mail']
        rol = data['rol']

        if not mail or not rol:
            return jsonify({'mensaje':'Faltan datos obligatorios'}), 400
        
        payload = {
            'mail': mail,
            'rol': rol,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'token':token}), 200
    
    def validar_token(self):
        token = request.headers['Authorization']

        if not token:
            return jsonify({"mensaje": "Token no proporcionado"}), 400

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return jsonify({"valid": True, "payload": decoded}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"valid": False, "mensaje": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"valid": False, "mensaje": "Token inválido"}), 401