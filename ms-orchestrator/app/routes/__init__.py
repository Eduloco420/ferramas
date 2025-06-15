from flask import Blueprint
from app.routes.root_routes import root_bp
from app.routes.producto_routes import producto_bp  
from app.routes.login_routes import login_bp
from app.routes.register_routes import register_bp
from app.routes.ventas_routes import venta_bp
from app.routes.img_routes import img_bp

def register_routes(app):
    app.register_blueprint(root_bp)
    app.register_blueprint(producto_bp, url_prefix='/productos')
    app.register_blueprint(login_bp, url_prefix='/auth')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(venta_bp, url_prefix='/venta')
    app.register_blueprint(img_bp, url_prefix='/img')
   