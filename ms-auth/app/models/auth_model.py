from app import mysql

class AuthModel:
    def obtener_usuario(self, mail):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM user WHERE mail = %s"
        cursor.execute(sql, (mail,))
        datos = cursor.fetchone()
        cursor.close()
        
        usuario = {
            'id':datos[0],
            'mail':datos[1],
            'rut':datos[2],
            'nombre':datos[3],
            'apellido':datos[4],
            'password':datos[5],
            'rol':datos[6]
        }

        return usuario