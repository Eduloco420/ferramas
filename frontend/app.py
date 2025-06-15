from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import jwt
import requests
import os
import functools



app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

JWT_SECRET = os.getenv('SECRET_KEY', 'tokenGen')


# Orquestador
URL_MS_ORCHESTRATOR = os.getenv("URL_MS_ORCHESTRATOR", "http://127.0.0.1:5009")
URL_FRONTEND = os.getenv("URL_FRONTEND", "http://127.0.0.1:3000")

@app.route('/')
def home():
    return render_template('home.html')

from flask import session, flash, redirect, url_for, render_template, request
import functools
import jwt

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')

        if not correo or not password:
            flash('Debes ingresar correo y contraseña')
            return render_template('login.html')

        datos = {"mail": correo, "password": password}

        try:
            r = requests.post(f"{URL_MS_ORCHESTRATOR}/auth/login", json=datos)
            if r.status_code == 200:
                respuesta = r.json()
                token = respuesta.get('token')

                if not token:
                    flash('No se recibió token de autenticación')
                    return render_template('login.html')

                payload = jwt.decode(token, options={"verify_signature": False})

                session['usuario_id'] = payload.get('id')
                session['usuario_nombre'] = payload.get('mail')
                session['usuario_rol'] = str(payload.get('rol'))
                session['token'] = token

                print("SESION DESPUES LOGIN:", dict(session))  # Debug

                flash(f"Bienvenido, {session['usuario_nombre']}")

                # Determinar la URL de redirección
                if session['usuario_rol'] == '1':
                    destino = url_for('dashboard_cliente')
                elif session['usuario_rol'] == '2':
                    destino = url_for('dashboard_trabajador')
                else:
                    destino = url_for('dashboard_general')

                print(f"Redirigiendo a: {destino}")  # Debug

                return redirect(destino)  # IMPORTANTE: return aquí

            else:
                flash(f"Error del servidor: código {r.status_code}")
                return render_template('login.html')

        except Exception as e:
            flash(f"Error al conectar con el servidor: {e}")
            return render_template('login.html')

    return render_template('login.html')

def login_required(rol_permitido=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            token = session.get('token')
            if not token:
                flash(" Debes iniciar sesión")
                return redirect(url_for('login'))

            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])  # ✅ FIX AQUÍ
                rol_actual = str(payload.get('rol'))

                if rol_permitido and rol_actual != str(rol_permitido):
                    flash(" No tienes permisos para acceder a esta página")
                    return redirect(url_for('login'))

                session['usuario_id'] = payload.get('id')
                session['usuario_rol'] = rol_actual
                session['usuario_nombre'] = payload.get('mail')

            except jwt.ExpiredSignatureError:
                flash(" Sesión expirada, por favor ingresa de nuevo")
                session.clear()
                return redirect(url_for('login'))
            except jwt.InvalidTokenError:
                flash(" Token inválido, inicia sesión nuevamente")
                session.clear()
                return redirect(url_for('login'))

            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/dashboard_cliente')
@login_required(rol_permitido='1')
def dashboard_cliente():
    return render_template('dashboard_cliente.html')


@app.route('/dashboard_trabajador')
@login_required(rol_permitido='2')
def dashboard_trabajador():
    return render_template('dashboard_trabajador.html')


@app.route('/dashboard_general')
@login_required()
def dashboard_general():
    return render_template('dashboard_general.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.")
    return redirect(url_for('login'))



@app.route('/register', methods=['GET', 'POST']) 
def registro():
    if request.method == 'POST':
        rol_str = request.form.get('rol')

        if not rol_str:
            return render_template("register.html", mensaje=" Debes seleccionar un rol.")

        datos = {
            "nombre": request.form.get('nombre'),
            "apellido": request.form.get('apellido'),
            "rut": request.form.get('rut'),
            "mail": request.form.get('mail'),
            "password": request.form.get('password'),
            "rol": int(rol_str)
        }

        try:
            r = requests.post(f"{URL_MS_ORCHESTRATOR}/register", json=datos)
            print(f"Orquestador response status: {r.status_code}")
            print(f"Orquestador response body: {r.text}")

            try:
                respuesta = r.json()
                mensaje_respuesta = respuesta.get("mensaje", "").lower()

                if "éxito" in mensaje_respuesta or "exito" in mensaje_respuesta:
                    # Enviar correo vía MS Orquestador con contenido HTML
                    try:
                        datos_correo = {
                            "para": datos["mail"],
                            "asunto": "¡Bienvenido a Ferremas!",
                            "contenido": f"""
                            <html>
                                <body>
                                    <p>Hola {datos['nombre']} {datos['apellido']},</p>
                                    <p>Gracias por registrarte en <strong>Ferremas</strong>. Estamos encantados de tenerte con nosotros.</p>
                                    <p>Ahora puedes disfrutar de todas nuestras funcionalidades.</p>
                                    <p>
                                        <a href="{URL_FRONTEND}/auth/login"" 
                                           style="background-color: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                                            Iniciar sesión
                                        </a>
                                    </p>
                                    <p>¡Gracias por unirte!</p>
                                    <p>El equipo de Ferremas</p>
                                </body>
                            </html>
                            """
                        }
                        correo_resp = requests.post(f"{URL_MS_ORCHESTRATOR}/notificaciones/correo", json=datos_correo)
                        if correo_resp.status_code != 200:
                            print("Error al enviar el correo:", correo_resp.text)
                    except Exception as e:
                        print("Excepción al enviar correo:", e)

                    mensaje = "✅ ¡Usuario creado con éxito! 😄🎉"
                    return render_template("register.html", mensaje=mensaje, mostrar_boton_login=True)

            except ValueError:
                pass  # Respuesta no fue JSON

            return render_template("register.html", mensaje=f" Error al registrar. Código {r.status_code}: {r.text}")

        except Exception as e:
            return render_template("register.html", mensaje=f" Error del servidor: {e}")

    return render_template("register.html")



@app.route('/productos')
def productos():
    try:
        r = requests.get(f"{URL_MS_ORCHESTRATOR}/productos/obtener")
        r.raise_for_status()
        productos = r.json()
        imagenes = {
            1: "taladro.jpg",
            2: "guanteseguri.jpg",
            3: "casco.jpeg",
            4: "cemento.jpg",
            5: "martillo.png",
            6: "carretilla.jpg",
            7: "pintura.jpeg",
            8: "pala.jpg",
            9: "guante.png"
        }
        for p in productos:
            p['imagen'] = imagenes.get(p.get('id'), 'default.png')
        return render_template('productos.html', productos=productos)
    except requests.exceptions.RequestException as req_err:
        return f"Error de conexión con el orquestador: {req_err}"
    except ValueError as val_err:
        return f"Error al decodificar JSON: {val_err}"
    except Exception as e:
        return f"Error al cargar productos: {e}"

    
@app.route('/producto/<int:producto_id>')
def producto_detalle(producto_id):
    try:
        r = requests.get(f"{URL_MS_ORCHESTRATOR}/productos/obtener/{producto_id}")
        if r.status_code == 200:
            producto = r.json()
            # Diccionario con IDs como enteros (no cadenas)
            imagenes = {
                1: "taladro.jpg",
                2: "guanteseguri.jpg",
                3: "casco.jpeg",
                4: "cemento.jpg",
                5: "martillo.png",
                6: "carretilla.jpg",
                7: "pintura.jpeg",
                8: "pala.jpg",
                9: "guante.png"
            }
            # Asignar imagen usando el ID entero
            producto['imagen'] = imagenes.get(producto.get("id"), "default.png")
            return render_template('producto_detalle.html', producto=producto)
        else:
            return render_template("error.html", mensaje="Producto no encontrado.")
    except Exception as e:
        return render_template("error.html", mensaje=str(e))


@app.route('/categoria/<string:nombre_categoria>')
def productos_por_categoria(nombre_categoria):
    try:
        r = requests.get(f"{URL_MS_ORCHESTRATOR}/productos/categoria/{nombre_categoria}")
        if r.status_code == 200:
            productos = r.json()
            imagenes = {
                "1": "taladro.jpg",
                "2": "guanteseguri.jpg",
                "C-2002": "casco.jpeg",
                "CP-3003": "cemento.jpg",
                "M-4004": "martillo.png",
                "CA-5005": "carretilla.jpg",
                "PL-6006": "pintura.jpeg",
                "P-7007": "pala.jpg",
                "G-1008": "guante.png"
            }
            for p in productos:
                p['imagen'] = imagenes.get(p.get("id", ""), "default.png")
            return render_template('productos_detalle.html', productos=productos, categoria=nombre_categoria)
        else:
            return render_template("error.html", mensaje="No se encontraron productos en esta categoría.")
    except Exception as e:
        return render_template("error.html", mensaje=str(e))



@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    data = request.get_json()
    producto_id = str(data.get('id'))  # siempre string para clave en session

    if not producto_id:
        return jsonify({"error": "ID de producto no proporcionado"}), 400

    carrito = session.get('carrito', {})

    # Aumentar cantidad si ya existe, sino agregar con cantidad 1
    if producto_id in carrito:
        carrito[producto_id] += 1
    else:
        carrito[producto_id] = 1

    session['carrito'] = carrito
    session.modified = True  # importante para actualizar sesión

    return jsonify({"mensaje": "Producto agregado al carrito"})

@app.route('/carrito')
def mostrar_carrito():
    carrito = session.get('carrito', {})

    # Obtener comunas desde el backend (orquestador)
    try:
        r_comunas = requests.get(f"{URL_MS_ORCHESTRATOR}/comunas/obtener")
        r_comunas.raise_for_status()
        comunas = r_comunas.json()
    except Exception as e:
        comunas = []
        # Puedes registrar el error en logs aquí

    if not carrito:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                "carrito": [],
                "total_carrito": 0,
                "mensaje": "El carrito está vacío.",
                "comunas": comunas
            })
        return render_template('carrito.html', carrito=[], total_carrito=0, mensaje="El carrito está vacío.", comunas=comunas)

    try:
        r = requests.get(f"{URL_MS_ORCHESTRATOR}/productos/obtener")
        r.raise_for_status()
        productos = r.json()

        productos_carrito = []
        total_carrito = 0

        for producto_id, cantidad in carrito.items():
            producto = next((p for p in productos if str(p['id']) == str(producto_id)), None)
            if producto:
                total = producto['precio'] * cantidad
                productos_carrito.append({
                    'id': producto['id'],
                    'nombre': producto['nombre'],
                    'precio': producto['precio'],
                    'cantidad': cantidad,
                    'total': total
                })
                total_carrito += total

        if request.headers.get('Accept') == 'application/json':
            return jsonify({
                "carrito": productos_carrito,
                "total_carrito": total_carrito,
                "comunas": comunas
            })

        return render_template('carrito.html', carrito=productos_carrito, total_carrito=total_carrito, mensaje=None, comunas=comunas)
    except Exception as e:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"error": str(e)}), 500
        return f"Error al cargar productos: {e}"


@app.route('/ver_carrito_sesion')
def ver_carrito_sesion():
    carrito = session.get('carrito', {})
    return jsonify(carrito)

@app.route('/modificar_carrito', methods=['POST'])
def modificar_carrito():
    data = request.get_json()
    action = data.get('action')
    producto_id = str(data.get('id'))

    carrito = session.get('carrito', {})

    if producto_id not in carrito:
        return jsonify({"error": "Producto no encontrado en carrito"}), 404

    if action == 'aumentar':
        carrito[producto_id] += 1
    elif action == 'disminuir':
        carrito[producto_id] -= 1
        if carrito[producto_id] <= 0:
            carrito.pop(producto_id)
    elif action == 'eliminar':
        carrito.pop(producto_id)
    else:
        return jsonify({"error": "Acción inválida"}), 400

    session['carrito'] = carrito
    session.modified = True

    return jsonify({"mensaje": "Carrito actualizado"})

@app.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    session.pop('carrito', None)
    return jsonify({"mensaje": "Carrito vaciado"})


@app.route('/cambiar_cantidad', methods=['POST'])
def cambiar_cantidad():
    producto_id = request.form.get('producto_id')
    accion = request.form.get('accion')  # 'sumar' o 'restar'
    carrito = session.get('carrito', {})

    if producto_id in carrito:
        if accion == 'sumar':
            carrito[producto_id] += 1
        elif accion == 'restar':
            carrito[producto_id] -= 1
            if carrito[producto_id] <= 0:
                del carrito[producto_id]
        session['carrito'] = carrito

    return redirect(url_for('mostrar_carrito'))



@app.route('/ventas')
def ventas_list():
    try:
        r = requests.get(f"{URL_MS_ORCHESTRATOR}/ventas")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pago', methods=['POST'])
def procesar_pago():
    datos = request.json
    try:
        r = requests.post(f"{URL_MS_ORCHESTRATOR}/pago", json=datos)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/enviar_correo', methods=['POST'])
def enviar_correo():
    datos = request.json
    try:
        r = requests.post(f"{URL_MS_ORCHESTRATOR}/mail", json=datos)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verificar_token', methods=['POST'])
def verificar_token():
    datos = request.json
    try:
        r = requests.post(f"{URL_MS_ORCHESTRATOR}/token/verificar", json=datos)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generar_token', methods=['POST'])
def generar_token():
    datos = request.json
    try:
        r = requests.post(f"{URL_MS_ORCHESTRATOR}/token/generar", json=datos)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)