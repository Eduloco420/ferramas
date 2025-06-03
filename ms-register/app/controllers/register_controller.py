from flask import jsonify, request
from app.models.register_model import registerModel
import bcrypt 
from rut_chile import rut_chile

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

            return jsonify({'mensaje':'Usuario creado con exito', 'id':user_id}), 200
        except Exception as e:
            return jsonify({'mensaje':'Error creando al usuario', 'Error':str(e)})