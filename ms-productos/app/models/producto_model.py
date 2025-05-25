from app import mysql

class ProductoModel:
    def obtener_todos(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM producto")
        datos = cursor.fetchall()
        cursor.close()

        productos = []
        for d in datos:
            productos.append({
                'id':d[0],
                'nombre':d[1],
                'marca':d[2],
                'codigo':d[3],
                'precio':d[4],
                'vigente':d[5]
            })
            
        return productos
    
    def obtener_precio(self, id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT precio FROM producto where id = %s", (id, ))
        datos = cursor.fetchone()
        cursor.close()

        precio = datos[0]
        return precio
    
    def insertar(self, nombre, marca, codigo, precio):
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO producto (nombre, marca, codigo, precio, vigente) VALUES (%s, %s, %s, %s, 1)"
        valores = (nombre, marca, codigo, precio)
        cursor.execute(sql, valores)
        mysql.connection.commit()
        cursor.close()

    def modificar(self, id, nombre, marca, codigo, precio, vigente):
        cursor = mysql.connection.cursor()
        sql = "UPDATE producto SET nombre = %s, marca = %s, codigo = %s, precio = %s, vigente = %s WHERE id = %s"
        valores = (nombre, marca, codigo, precio, vigente, id)
        cursor.execute(sql, valores)
        mysql.connection.commit()
        cursor.close()
