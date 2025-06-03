import jwt
import datetime
from flask import request, jsonify
import bcrypt
from app.models.auth_model import AuthModel
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.getenv('SECRET_KEY')

class AuthController:
    def __init__(self):
        self.modelo = AuthModel()

    def login(self):
        try:
            data = request.get_json()
            mail = data.get('mail')
            password = data.get('password')

            usuario = self.modelo.obtener_usuario(mail)

            if not usuario:
                return jsonify({'mensaje':'Usuario no encontrado'}),404
            
            if not bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
                return jsonify({'mensaje': 'Contraseña incorrecta'}), 401
            
            payload = {
                'mail': usuario['mail'],
                'rol': usuario['rol'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({'token': token}), 200

        except Exception as e:
            return jsonify({'mensaje':'Ha ocurrido un error durante el inicio de sesión', 'Error':str(e)}), 400

    def validar_token(self):
        token = request.headers['Authorization']
        try:
            return jwt.decode(token, SECRET_KEY, algorithms='HS256')
        except jwt.exceptions.DecodeError:
            response = jsonify({"mensaje":"Token Invalido"})
            response.status_code = 401
            return response
        except jwt.exceptions.ExpiredSignatureError:
            response = jsonify({"mensaje":"Token Expirado"})
            response.status_code = 401
            return response

