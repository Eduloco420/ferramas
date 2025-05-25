from app import mysql

class PagoModel:
    def obtener_todos(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM pago")
        datos = cursor.fetchall()
        pagos = []
        for d in datos:
            pagos.append({
                'id':d[0],
                'venta':d[1],
                'montoPago':d[2],
                'token':d[3],
                'status':d[4],
                'cardDetail':d[5],
                'transactionDate':d[6]
            })

        return pagos
    
    def ingresar_pago(self, venta, montoPago, token):
        cursor = mysql.connection.cursor()
        sql = 'INSERT INTO pago (venta, montoPago, token, status) VALUES (%s, %s, %s, "INITIALIZED") '
        cursor.execute(sql, (venta, montoPago, token))
        mysql.connection.commit()
        cursor.close()

    def actualizar_pago(self, token, status, card_detail, transaction_date):
        cursor = mysql.connection.cursor()
        sql = "UPDATE pago SET status = %s, card_detail = %s, transaction_date = %s WHERE token = %s;"
        cursor.execute(sql, (status, card_detail, transaction_date, token))
        mysql.connection.commit()

        sql = "SELECT venta FROM pago WHERE token = %s"
        cursor.execute(sql, (token,))
        datos = cursor.fetchone()
        venta = datos[0]
        cursor.close()
        
        return venta 

