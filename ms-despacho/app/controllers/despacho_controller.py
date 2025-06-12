from flask import jsonify, request
from app.models.despacho_model import DespachoModel

class DespachoController:
    def __init__(self):
        self.modelo = DespachoModel()

    def listar_despachos(self):
        despachos = self.modelo.obtener_todos()
        return despachos
    
    def ver_despacho(self, id):
        despacho = self.modelo.ver_despacho(id)
        if despacho is None:
            return jsonify({'mensaje':'No se encontraron datos'}), 404
        return despacho
    
    def ingresar_despacho(self):
        datos = request.get_json()
        venta = datos['venta']
        direccion = datos['direccion']
        comuna = datos['comuna']

        if not venta or not direccion or not comuna:
            return jsonify({'mensaje':'Para ingresar se debe indicar venta, direccion y comuna'}), 400

        try:
            self.modelo.ingresar_despacho(venta=venta, direccion=direccion, comuna=comuna)
            return jsonify({'mensaje':'despacho ingresado con exito'}), 200
        except Exception as e:
            return jsonify({'mensaje':'Error ingresando despacho', 'Error':str(e)}), 400
        
