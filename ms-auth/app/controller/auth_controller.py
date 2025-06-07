import datetime
from flask import request, jsonify
import bcrypt
from app.models.auth_model import AuthModel
from dotenv import load_dotenv
import os
import requests

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
            }

            data = requests.post('http://127.0.0.1:5006/token/generar', json=payload)

            token = data['token']

            return token

        except Exception as e:
            return jsonify({'mensaje':'Ha ocurrido un error durante el inicio de sesión', 'Error':str(e)}), 400