from flask import jsonify, request
from app.models.register_model import registerModel
import bcrypt 
from rut_chile import rut_chile
import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

URL_MS_MAIL = os.getenv('URL_MS_MAIL')

class registerController:
    def __init__(self):
        self.modelo = registerModel()

    def crear_usuario(self):
        try:
            data = request.get_json()
            password = data.get('password')
            rut = data.get('rut')
            salt = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            if not rut_chile.is_valid_rut(rut):
                return jsonify({'mensaje':'Rut erroneo, favor ingresar un Rut valido'})
            
            user = {
                'mail': data.get('mail'),
                'rut': rut,
                'nombre': data.get('nombre'),
                'apellido': data.get('apellido'),
                'password': hash_password.decode('utf-8'),
                'rol': data.get('rol')
            }
            user_id = self.modelo.registar_usuario(user=user)

            cuerpo = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
                        <div style="max-width: 600px; margin: auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <div style="background-color: #007bff; padding: 20px; color: white; text-align: center;">
                            <h2>¡Bienvenido a Ferremas!</h2>
                        </div>
                        <div style="padding: 30px;">
                            <p>Hola <strong>{user['nombre']} {user['apellido']}</strong>,</p>
                            <p>Gracias por registrarte en <strong>Ferremas</strong>. Estamos encantados de tenerte con nosotros.</p>
                            <p>Ahora puedes disfrutar de todas nuestras funcionalidades.</p>
                            <p style="text-align: center; margin: 30px 0;">
                            <a href="https://tusitio.com/login" style="background-color: #007bff; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px;">Iniciar sesión</a>
                            </p>
                            <p>¡Gracias por unirte!</p>
                            <p>El equipo de <strong>Ferremas</strong></p>
                        </div>
                        <div style="background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                            © 2025 Ferremas. Todos los derechos reservados.
                        </div>
                        </div>
                    </body>
                    </html>
                    """

            mail = {
                'destinatario':user['mail'],
                'asunto':'Usuario registrado con exito',
                'cuerpo':cuerpo
            }

            requests.post(f'{URL_MS_MAIL}/mail', json=mail)

            return jsonify({'mensaje':'Usuario creado con exito', 'id':user_id}), 200
        except Exception as e:
            return jsonify({'mensaje':'Error creando al usuario', 'Error':str(e)})