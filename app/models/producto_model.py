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
    
    def insertar(self, nombre, marca, codigo, precio, vigente):
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO producto (nombre, marca, codigo, precio, vigente) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, marca, codigo, precio, vigente)
        cursor.execute(sql, valores)
        mysql.connection.commit()
        cursor.close()

    