from app import mysql

class DespachoModel:
    def obtener_todos(self):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM despacho"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursor.close()

        despachos = []
        for d in datos:
            despachos.append({
                'id':d[0],
                'estadoDespacho':d[1],
                'fecEstado':d[2],
                'venta':d[3],
                'direccion':d[4],
                'comuna':d[5]
            })

        return despachos
    
    def ver_despacho(self, id):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM despacho where id = %s"
        cursor.execute(sql, (id, ))
        datos = cursor.fetchone()
        cursor.close()

        if datos is None:
            return None

        despacho = {
            'id':datos[0],
            'estadoDespacho':datos[1],
            'fecEstado':datos[2],
            'venta':datos[3],
            'direccion':datos[4],
            'comuna':datos[5]
        }

        return despacho
    
    def ingresar_despacho(self, venta, direccion, comuna):
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO despacho (estadoDespacho, fecEstado, venta, direccion, comuna) VALUES ('Pendiente despacho', now(), %s, %s, %s)"
        cursor.execute(sql,( venta, direccion, comuna))
        cursor.close()
        mysql.connection.commit()


        
