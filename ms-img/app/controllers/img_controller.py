from flask import jsonify, request, send_from_directory
from app.models.img_model import imgModel
from config import Config
import json
import uuid
import os

class imgController:
    def __init__(self):
        self.modelo = imgModel()
        self.image_folder = Config.IMAGE_FOLDER

    def ver_imagen(self, filename):
        return send_from_directory(self.image_folder, filename)

    def imagenes_producto(self, id):
        img_tuplas = self.modelo.obtener_img(id)
        img_list = [img[0] for img in img_tuplas]

        return jsonify(img_list)
    
    def listar_imagenes(self):
        archivos = os.listdir(self.image_folder)
        return archivos
    
    def cargar_img(self):
        images = request.files.getlist('img')
        producto_id = request.form.get('id')

        for img in images:
            if img.filename != '':
                ext = os.path.splitext(img.filename)[1]
                nombreArchivo = f"{producto_id}_{uuid.uuid4().hex}{ext}"
                ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombreArchivo)