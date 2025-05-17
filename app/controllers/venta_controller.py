from flask import jsonify, request
from app.models.venta_model import VentaModel
from app.models.producto_model import ProductoModel
from app import mysql


class VentaController:
    def __init__(self):
        self.modelo = VentaModel()
        self.modelo_producto = ProductoModel()


    def listar_ventas(self):
        productos = self.modelo.obtener_todos()
        return jsonify(productos), 200
    
    def agregar_venta(self):
        datos = request.get_json()
        cliente = datos.get('cliente')
        productos = datos.get('productos')

        if not all([cliente, productos is not None]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        detalle_productos = []
        valor_total = 0   

        for p in productos:
            producto = p.get('producto')
            cant = p.get('cant')

            if not all([producto, cant]):
                return jsonify({'error': 'Faltan datos de producto'}), 400

            precio_producto = self.modelo_producto.obtener_precio(producto)

            if not precio_producto:
                return jsonify({'error': f'Producto con ID {producto} no encontrado'}), 404

            valor_producto = precio_producto * cant
            valor_total += valor_producto

            detalle_productos.append({
                'producto':producto,
                'cant':cant,
                'valor_unitario':precio_producto,
                'valor_total':valor_total
            })

        connection = mysql.connection
        cursor = connection.cursor()

        try:
            venta_id = self.modelo.ingresar(cliente, valor_total)

            for prod in detalle_productos:
                self.modelo.ingresar_detalle(venta_id, prod['producto'], prod['cant'])

            connection.commit()

            return jsonify({'mensaje':'Se a ingresado correctamente la venta', 'venta_id':venta_id, 'detalle':detalle_productos})

        except Exception as e:
            return 'hola'            
                


        
