from app import mysql

class VentaModel:
    def obtener_todos(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM ventas")
        datos = cursor.fetchall()
        cursor.close()

        ventas = []
        for d in datos:
            ventas.append({
                'id':d[0],
                'cliente':d[1],
                'fecVenta':d[2],
                'valorVenta':d[3],
                'EstadoVenta':d[4]
            })

        return ventas
    
    def ingresar(self, cursor, cliente, valor_total):
        sql = "INSERT INTO ventas (cliente, fecVenta, valorVenta, estadoVenta) VALUES (%s, now(), %s, 'Pendiente')"
        cursor.execute(sql, (cliente, valor_total))

        venta_id = cursor.lastrowid
        return venta_id
    
    def ingresar_detalle(self, cursor, venta, producto, cant):
        sql = "INSERT INTO detalleVentas (venta, producto, cantidad) VALUES (%s,%s,%s)"
        cursor.execute(sql, (venta, producto, cant))

        cursor.close()
        
