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
URL_MS_TOKEN = os.getenv('URL_MS_TOKEN')

class AuthController:
    def __init__(self):
        self.modelo = AuthModel()

    def login(self):
        try:
            data = request.get_json()
            mail = data.get('mail')
            password = data.get('password')

            usuario = self.modelo.obtener_usuario(mail)

            print(usuario)

            if not usuario:
                return jsonify({'mensaje':'Usuario no encontrado'}),404
            
            if not bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
                return jsonify({'mensaje': 'Contraseña incorrecta'}), 401
            
            payload = {
                'mail': usuario['mail'],
                'rol': usuario['rol'],
                'id': usuario['id']
            }

            response = requests.post(f'{URL_MS_TOKEN}/token/generar', json=payload)

            print('Status Code:', response.status_code)
            print('Response Text:', response.text)  

            if response.status_code != 200:
                return jsonify({'mensaje': 'Error al generar el token', 'detalle': response.text}), 500

            token_data = response.json()
            token = token_data.get('token')

            return jsonify({'token': token}), 200

        except Exception as e:
            return jsonify({'mensaje':'Ha ocurrido un error durante el inicio de sesión', 'Error':str(e)}), 400