from flask import jsonify

def lista_producto(con):
    cursor = con.connection.cursor()
    sql = "SELECT * FROM producto"
    cursor.execute(sql)
    datos = cursor.fetchall()
    productos = []
    for d in datos:
        producto = {'id':d[0],
                    'nombre':d[1],
                    'marca':d[2],
                    'codigo':d[3],  
                    'precio':int(d[4])}
        productos.append(producto)
    return jsonify({'productos':productos})        
