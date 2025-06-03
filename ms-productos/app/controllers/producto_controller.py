from flask import jsonify, request
from app.models.producto_model import ProductoModel

class ProductoController:
    def __init__(self):
        self.modelo = ProductoModel()

    def listar_productos(self):
        productos = self.modelo.obtener_todos()
        return jsonify(productos)
    
    def listar_producto(self, id):
        try:
            producto = self.modelo.obtener_producto(id)
            if producto['vigente'] == 0:
                return jsonify({'mensaje':'Producto no vigente'})
            return producto 
        except Exception as e:
            return jsonify({'mensaje':'Error buscando producto', 'Error': str(e)})
    
    def ver_precio(self, id):
        precio = self.modelo.obtener_precio(id)
        return str(precio)
    
    def agregar_producto(self):
        datos = request.get_json()
        nombre = datos.get('nombre')
        marca = datos.get('marca')
        codigo = datos.get('codigo')
        precio = datos.get('precio')

        if not all([nombre, marca, codigo, precio is not None]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        self.modelo.insertar(nombre, marca, codigo, precio)
        return jsonify({'mensaje': 'Producto agregado correctamente'}), 201

    def modificar_producto(self, id):
        datos = request.get_json()
        nombre = datos.get('nombre')
        marca = datos.get('marca')
        codigo = datos.get('codigo')
        precio = datos.get('precio')
        vigente = datos.get('vigente')

        if not all([nombre, marca, codigo, precio, vigente is not None ]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
        
        self.modelo.modificar(id, nombre, marca, codigo, precio, vigente)
        return jsonify({'mensaje':'Producto modificado correctamente',}),201