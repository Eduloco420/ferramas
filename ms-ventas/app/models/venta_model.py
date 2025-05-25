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

    def obtener_venta(self, id):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM ventas WHERE id = %s"
        cursor.execute(sql, (id,))
        datos = cursor.fetchone()
        venta ={
                    'id':datos[0],
                    'cliente':datos[1],
                    'fecVenta':datos[2],
                    'valorVenta':datos[3],
                    'EstadoVenta':datos[4]
                }
        
        return venta
    
    def ingresar(self, cursor, cliente, valor_total):
        sql = "INSERT INTO ventas (cliente, fecVenta, valorVenta, estadoVenta) VALUES (%s, now(), %s, 'Pendiente')"
        cursor.execute(sql, (cliente, valor_total))

        venta_id = cursor.lastrowid
        return venta_id
    
    def ingresar_detalle(self, cursor, venta, producto, cant):
        sql = "INSERT INTO detalleVentas (venta, producto, cantidad) VALUES (%s,%s,%s)"
        cursor.execute(sql, (venta, producto, cant))                

    def cambiar_estado(self, venta, estado):
        cursor = mysql.connection.cursor()
        sql = "UPDATE ventas SET estadoVenta = %s WHERE id = %s"
        cursor.execute(sql, (estado, venta))
        mysql.connection.commit()