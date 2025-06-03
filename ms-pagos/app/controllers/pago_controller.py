from flask import jsonify, request
from app.models.pago_model import PagoModel
import requests
import time
from datetime import datetime
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

WEBPAY = os.getenv('WEBPAY')
RETORNO = os.getenv('RETORNO')
KEY_ID = os.getenv('KEY_ID')
KEY_SECRET = os.getenv('KEY_SECRET')

class PagoController:
    def __init__(self):
        self.modelo = PagoModel()

    def listar_pagos(self):
        pagos = self.modelo.obtener_todos()
        return jsonify(pagos)

    def ingresar_pago(self):
        datos = request.get_json()
        venta = datos['venta']
        
        response = requests.get(f'http://127.0.0.1:5001/venta/{venta}')

        if response.status_code == 200:
            data = response.json()
            monto_venta = float(data['valorVenta'])
            cliente = data['cliente']
            estado = data['EstadoVenta']
        else:
            return jsonify({'mensaje':'error llamando al servicio'}), 400

        if not monto_venta:
            return jsonify({'mensaje':f'No se ha encontrado la venta {venta}'}), 404
        
        if estado is not "Pendiente":
            return jsonify({'mensaje':'Venta ya se encuentra pagada'}), 418
        
        buy_order = f'venta{venta}id{int(time.time())}'
        session_id = f'sesion{cliente}{int(time.time())}'

        payload = {
            'buy_order':buy_order,
            'session_id':session_id,
            'amount':monto_venta,
            'return_url':RETORNO
        }

        headers = {
            'Content-Type': 'application/json',
            'Tbk-Api-Key-Id': KEY_ID,
            'Tbk-Api-Key-Secret': KEY_SECRET 
        }

        response = requests.post(url=f'{WEBPAY}/rswebpaytransaction/api/webpay/v1.2/transactions', json=payload, headers=headers)

        data = response.json()

        self.modelo.ingresar_pago(venta=venta, montoPago=monto_venta, token=data['token'])                        

        return data
    
    def confirmar_pago(self):
        data = request.get_json()
        token = data['token_ws']

        headers = {
            'Content-Type': 'application/json',
            'Tbk-Api-Key-Id': KEY_ID,
            'Tbk-Api-Key-Secret': KEY_SECRET 
        }

        response = requests.put(f'{WEBPAY}/rswebpaytransaction/api/webpay/v1.2/transactions/{token}', headers=headers)

        data = response.json()
        card_detail = data['card_detail']
        transaction_date = data['transaction_date']
        transaction_date = datetime.strptime(transaction_date.replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f")
        transaction_date = transaction_date.strftime("%Y-%m-%d %H:%M:%S")

        venta = self.modelo.actualizar_pago(token=token, status=data['status'], card_detail=card_detail['card_number'], transaction_date=transaction_date)

        print(venta)
        
        if data['status'] == 'AUTHORIZED':
            payload = {
                'estado':'Pagado'
            }
            requests.put(f'http://127.0.0.1:5001/venta/{venta}', json=payload)
            

        return data


