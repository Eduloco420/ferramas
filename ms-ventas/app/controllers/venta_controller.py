from flask import jsonify, request
from app.models.venta_model import VentaModel
from app import mysql
import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

URL_MS_PRODUCTO = os.getenv('URL_MS_PRODUCTO')
URL_MS_DESPACHO = os.getenv('URL_MS_DESPACHO')

class VentaController:
    def __init__(self):
        self.modelo = VentaModel()

    def listar_ventas(self):
        venta = self.modelo.obtener_todos()
        return venta
    
    def ver_venta(self, id):
        venta = self.modelo.obtener_venta(id)
        return venta
    
    def agregar_venta(self):
        datos = request.get_json()
        cliente = datos.get('cliente')
        productos = datos.get('productos')
        despacho = datos.get('despacho')
        direccion = despacho.get('direccion')
        comuna = despacho.get('comuna')

        if not all([cliente, productos, direccion, comuna is not None]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        detalle_productos = []
        valor_total = 0

        for p in productos:
            producto = p.get('producto')
            cant = p.get('cant')

            if not all([producto, cant]):
                return jsonify({'error': 'Faltan datos de producto'}), 400

            response = requests.get(f'{URL_MS_PRODUCTO}/productos/precio/{producto}')

            if response.status_code == 200:
                data = response.text
                precio_producto = float(data)
            else:
                return jsonify({'mensaje':'error llamando al servicio'}), 400

            if not precio_producto:
                return jsonify({'mensaje': f'Producto con ID {producto} no encontrado'}), 404

            valor_producto = precio_producto * cant
            valor_total += valor_producto

            detalle_productos.append({
                'producto':producto,
                'cant':cant,
                'valor_unitario':precio_producto,
                'valor_total':valor_producto
            })

        connection = mysql.connection
        cursor = connection.cursor()
        connection.begin()

        try:
            venta_id = self.modelo.ingresar(cursor, cliente, valor_total)

            for prod in detalle_productos:
                self.modelo.ingresar_detalle(cursor, venta_id, prod['producto'], prod['cant'])                

            connection.commit()

            payload = {
                'venta': venta_id,                    
                'direccion':direccion,
                'comuna':comuna
            }
            
            despacho = requests.post(f'{URL_MS_DESPACHO}/despacho', json=payload)
            despacho = despacho.json()

            return jsonify({'mensaje':'Se a ingresado correctamente la venta', 'venta_id':venta_id, 'detalle':detalle_productos, 'despacho': despacho})

        except Exception as e:
            connection.rollback()
            return jsonify({'mensaje':'Error ingresando la venta', "error":str(e)}), 400
        
    def modificar_venta(self, venta):
        data = request.get_json()
        estado = data['estado']
        
        self.modelo.cambiar_estado(venta=venta, estado=estado)

        return jsonify({'mensaje':'Cambio realizado'})
