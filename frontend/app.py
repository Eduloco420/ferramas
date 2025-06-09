from flask import Flask, render_template, jsonify, request, session
import requests

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # necesario para usar sesión

# URLs base corregidas
MS_AUTH_URL = "http://127.0.0.1:5003"
MS_PRODUCTOS_URL = "http://127.0.0.1:5000"
MS_PAGOS_URL = "http://127.0.0.1:5002"
MS_REGISTER_URL = "http://127.0.0.1:5004"
MS_VENTAS_URL = "http://127.0.0.1:5001"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/auth')
def auth_info():
    try:
        r = requests.get(f"{MS_AUTH_URL}/verify/token")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = None
    if request.method == 'POST':
        datos = {
            "correo": request.form.get("correo"),
            "password": request.form.get("password")
        }
        try:
            r = requests.post(f"{MS_AUTH_URL}/login", json=datos)
            if r.status_code == 200:
                mensaje = "Inicio de sesión exitoso."
                # Aquí podrías guardar info en session si quieres
            else:
                mensaje = r.json().get("mensaje", "Error al iniciar sesión.")
        except Exception as e:
            mensaje = f"Error al conectar con ms-auth: {str(e)}"
    return render_template("login.html", mensaje=mensaje)

@app.route('/pagos')
def pagos_info():
    return jsonify({"mensaje": "ms-pagos no tiene endpoint GET para mostrar estado."})

@app.route('/productos')
def productos_list():
    try:
        r = requests.get(f"{MS_PRODUCTOS_URL}/productos")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/productos_html')
def productos_html():
    try:
        r = requests.get(f"{MS_PRODUCTOS_URL}/productos")
        productos = r.json()
        
        # Diccionario con imagenes por codigo o id
        imagenes = {
            "T-1234": "taladro.jpg",
            "G-1001": "guanteseguri.jpg",
            "C-2002": "casco.jpeg",
            "CP-3003": "cemento.jpg",
            "M-4004": "martillo.png",
            "CA-5005": "carretilla.jpg",  # si tienes esta imagen
            "PL-6006": "pintura.jpeg",
            "P-7007": "pala.jpg",
            "G-1008": "guante.png"
        }
        
        # Agrega campo imagen a cada producto basado en codigo
        for p in productos:
            p['imagen'] = imagenes.get(p['codigo'], 'default.png')  # default.png si no está

        return render_template('productos.html', productos=productos)
    except Exception as e:
        return f"Error al cargar productos: {e}"


@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    producto_id = request.json.get('id')
    if not producto_id:
        return jsonify({"error": "Falta id del producto"}), 400

    carrito = session.get('carrito', [])
    if producto_id not in carrito:
        carrito.append(producto_id)
        session['carrito'] = carrito
    else:
        return jsonify({"mensaje": "Producto ya está en el carrito", "carrito": carrito}), 200

    return jsonify({"mensaje": f"Producto {producto_id} agregado al carrito", "carrito": carrito})

@app.route('/register', methods=['GET'])
def mostrar_formulario_registro():
    return render_template('registro.html')

@app.route('/register', methods=['POST'])
def procesar_formulario_registro():
    usuario = request.form.get('usuario')
    clave = request.form.get('clave')
    email = request.form.get('email')

    datos = {
        "usuario": usuario,
        "clave": clave,
        "email": email
    }

    try:
        r = requests.post(f"{MS_REGISTER_URL}/registro", json=datos)

        if r.status_code == 201:
            return render_template("login.html", mensaje="✅ Registro exitoso.")
        else:
            return render_template("registro.html", mensaje="❌ Error en el registro.")
    except Exception as e:
        return render_template("registro.html", mensaje=f"⚠️ Error al registrar: {str(e)}")

@app.route('/ventas')
def ventas_list():
    try:
        r = requests.get(f"{MS_VENTAS_URL}/venta")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/carrito')
def mostrar_carrito():
    carrito = session.get('carrito', [])

    if not carrito:
        return render_template('carrito.html', productos=[], mensaje="El carrito está vacío.")

    try:
        r = requests.get(f"{MS_PRODUCTOS_URL}/productos")
        productos = r.json()
        productos_carrito = [p for p in productos if p['id'] in carrito]
        return render_template('carrito.html', productos=productos_carrito, mensaje=None)
    except Exception as e:
        return f"Error al cargar productos: {e}"

@app.route('/carrito/vaciar', methods=['POST'])
def vaciar_carrito():
    session['carrito'] = []
    return jsonify({"mensaje": "Carrito vaciado correctamente."})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
