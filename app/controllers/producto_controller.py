from flask import jsonify, request
from app.models.producto_model import ProductoModel

class ProductoController:
    def __init__(self):
        self.modelo = ProductoModel()

    def listar_productos(self):
        productos = self.modelo.obtener_todos()
        return jsonify(productos)
    
    def agregar_producto(self):
        datos = request.get_json()
        nombre = datos.get('nombre')
        marca = datos.get('marca')
        codigo = datos.get('codigo')
        precio = datos.get('precio')
        vigente = datos.get('vigente')

        if not all([nombre, marca, codigo, precio, vigente is not None]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        self.modelo.insertar(nombre, marca, codigo, precio, vigente)
        return jsonify({'mensaje': 'Producto agregado correctamente'}), 201