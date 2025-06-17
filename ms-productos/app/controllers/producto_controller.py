from flask import jsonify, request
from app.models.producto_model import ProductoModel
import os
import requests
from dotenv import load_dotenv
import math

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

URL_MS_IMG = os.getenv('URL_MS_IMG')

class ProductoController:
    def __init__(self):
        self.modelo = ProductoModel()

    def listar_productos(self):
        productos = self.modelo.obtener_todos()
        for p in productos:
            id = p['id']
            img_respose = requests.get(f'{URL_MS_IMG}/img/producto/{id}')
            img_data = img_respose.json() or None
            
            p['imagenes'] = img_data

        return jsonify(productos)
    
    def listar_producto(self, id):
        try:
            producto = self.modelo.obtener_producto(id)
            if not producto:
                return jsonify({'mensaje': 'Producto no encontrado'}), 404
            
            if producto['vigente'] == 0:
                return jsonify({'mensaje':'Producto no vigente'})
            img_respose = requests.get(f'{URL_MS_IMG}/img/producto/{id}')
            img_data = img_respose.json()
            producto['imagenes'] = img_data
            return jsonify(producto) 
        except Exception as e:
            return jsonify({'mensaje':'Error buscando producto', 'Error': str(e)})
    
    def ver_precio(self, id):
        precio = self.modelo.obtener_precio(id)
        return str(precio)
    
    def agregar_producto(self):
        datos = request.get_json()
        print(datos)
        nombre = datos.get('nombre')
        marca = datos.get('marca')
        codigo = datos.get('codigo')
        precio = datos.get('precio')

        if not all([nombre, marca, codigo, precio is not None]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        producto_id = self.modelo.insertar(nombre, marca, codigo, precio)

        return jsonify({'mensaje': 'Producto agregado correctamente', 'producto':producto_id}), 201

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

    def buscar_productos(self):
        search = request.args.get('search')
        pagina = request.args.get('pagina')
        pagina = int(pagina)
        cant_prod = 12 
        offset = (pagina - 1) * cant_prod

        try:
            total_prod = self.modelo.cant_productos(search)

            if total_prod == 0 or total_prod == None:
                return jsonify({'mensaje':'No se han encontrado productos'}), 404

            total_pag = int(math.ceil(total_prod/cant_prod))
            productos = self.modelo.buscar_productos(search,cant_prod,offset)
            response = {
                'paginaActual':pagina,
                'cantPaginas':total_pag,
                'productos':productos,
                'cantProductos':total_prod
            }

            return jsonify(response),200
        except Exception as e:
            return jsonify({'mensaje':'Error obteniendo los datos', 'Error':str(e)})