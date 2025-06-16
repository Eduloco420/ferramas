from flask import jsonify, request, Response, make_response
import requests
import os
from dotenv import load_dotenv

# Cargar .env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

# URLs de microservicios
URL_MS_PRODUCTO = os.getenv('URL_MS_PRODUCTO')
URL_MS_VENTA = os.getenv('URL_MS_VENTA')
URL_MS_PAGOS = os.getenv('URL_MS_PAGOS')
URL_MS_AUTH = os.getenv('URL_MS_AUTH')
URL_MS_REGISTER = os.getenv('URL_MS_REGISTER')
URL_MS_MAIL = os.getenv('URL_MS_MAIL')
URL_MS_TOKEN = os.getenv('URL_MS_TOKEN')
URL_MS_DESPACHO = os.getenv('URL_MS_DESPACHO')
URL_MS_IMG = os.getenv('URL_MS_IMG')

MICROSERVICIOS = {
    'ms-Producto': URL_MS_PRODUCTO,
    'ms-Venta': URL_MS_VENTA,
    'ms-Pagos': URL_MS_PAGOS,
    'ms-Auth': URL_MS_AUTH,
    'ms-Register': URL_MS_REGISTER,
    'ms-Mail': URL_MS_MAIL,
    'ms-Token': URL_MS_TOKEN,
    'ms-Despacho': URL_MS_DESPACHO,
    'ms-Imagen': URL_MS_IMG
}

class OrchestratorController:
    def home(self):
        return "Si ves esto, es porque el servicio está funcionando (creo...)"

    def ms_status(self):
        resultados = {}
        for nombre, url in MICROSERVICIOS.items():
            if not url:
                continue
            try:
                response = requests.get(url, timeout=2)
                resultados[nombre] = {
                    'url': url,
                    'estado': 'activo',
                    'codigo_http': response.status_code
                }
            except requests.exceptions.RequestException as e:
                resultados[nombre] = {
                    'url': url,
                    'estado': 'inactivo',
                    'error': str(e)
                }
        return resultados
    
    def obtener_producto(self, id):
        try:
            response = requests.get(f'{URL_MS_PRODUCTO}/productos/{id}')
            response.raise_for_status()
            return jsonify(response.json()), response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Producto no encontrado', 'Error': str(e)}), 404


    def crear_producto(self):
        nombre = request.form.get('nombre')
        marca = request.form.get('marca')
        codigo = request.form.get('codigo')
        precio = request.form.get('precio')
        images = request.files.getlist('images')

        if not all([nombre, marca, codigo, precio, images]):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        payload = {
            'nombre': nombre,
            'marca': marca,
            'codigo': codigo,
            'precio': precio
        }

        try:
            producto_response = requests.post(f'{URL_MS_PRODUCTO}/productos', json=payload)
            producto_response.raise_for_status()
            producto_data = producto_response.json()
            producto = producto_data['producto']

            files = [('images', (img.filename, img.stream, img.mimetype)) for img in images]
            data_form = {'id': producto}
            img_response = requests.post(f'{URL_MS_IMG}/img/cargar', files=files, data=data_form)
            img_data = img_response.json()

            return jsonify({
                'mensaje': 'Producto creado con Éxito',
                'producto': producto_data,
                'imagenes': img_data
            }), 201
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Error al comunicar con microservicios', 'detalle': str(e)}), 500
        except Exception as e:
            return jsonify({'mensaje': 'Error creando el producto', 'Error': str(e)}), 500

    def obtener_productos(self):
        try:
            producto_response = requests.get(f'{URL_MS_PRODUCTO}/productos')
            producto_data = producto_response.json()
            return producto_data
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def modificar_producto(self, id):
        try:
            data = request.get_json()
            response = requests.put(f'{URL_MS_PRODUCTO}/productos/{id}', json=data)
            response_data = response.json()
            return response_data, response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def login(self):
        try:
            data = request.get_json()
            response = requests.post(f'{URL_MS_AUTH}/login', json=data)
            login_data = response.json()
            return login_data, response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def register(self):
        try:
            data = request.get_json()
            response = requests.post(f'{URL_MS_REGISTER}/register', json=data)
            register_data = response.json()
            return register_data, response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500


    def validar_token(self):
        try:
            token = request.headers.get('Authorization')
            response = requests.post(f'{URL_MS_TOKEN}/token/validar', headers={'Authorization': token})
            token_data = response.json()
            return token_data, response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def ingresar_venta(self):
        try:
            data = request.get_json()
            token = request.headers.get('Authorization')
            venta_response = requests.post(f'{URL_MS_VENTA}/venta', json=data, headers={'Authorization': token})
            venta_data = venta_response.json()
            venta_id = venta_data.get('venta_id')

            payload = {"venta": venta_id}
            pago_response = requests.post(f'{URL_MS_PAGOS}/pago', json=payload)
            pago_data = pago_response.json()

            venta_data['pago'] = pago_data
            return venta_data, venta_response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def obtener_ventas(self):
        try:
            response = requests.get(f'{URL_MS_VENTA}/venta')
            ventas_data = response.json()
            return ventas_data, response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def obtener_venta(self, id):
        try:
            response = requests.get(f'{URL_MS_VENTA}/venta/{id}')
            venta_data = response.json()
            return venta_data, response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def cambiar_estado_venta(self, id):
        raise NotImplementedError("Esta función aún no ha sido implementada.")

    def ver_imagen(self, filename):
        try:
            response = requests.get(f'{URL_MS_IMG}/img/archivo/{filename}', stream=True)
            if response.status_code != 200:
                return jsonify({'mensaje': 'No se pudo obtener la imagen'}), response.status_code
            return Response(
                response.iter_content(chunk_size=1024),
                content_type=response.headers.get('Content-Type')
            )
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

    def confirmar_pago(self):
        try:
            data = request.get_json()
            token_ws = data.get('token_ws')
            payload = {'token_ws': token_ws}
            pago_response = requests.post(f'{URL_MS_PAGOS}/pago/confirmar', json=payload)
            pago_data = pago_response.json()
            return pago_data, pago_response.status_code
        except Exception as e:
            return jsonify({'mensaje': 'Error conectando al servicio', 'Error': str(e)}), 500

