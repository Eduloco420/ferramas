from app import mysql

class registerModel:
    def registar_usuario(self, user):
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO user (mail, rut, nombre, apellido, password, rol) VALUES (%s, %s, %s, %s, %s, %s)"
        mail = user['mail']
        rut = user['rut']
        nombre = user['nombre']
        apellido = user['apellido']
        password = user['password']
        rol = user['rol']
        cursor.execute(sql, (mail, rut, nombre, apellido, password, rol))
        cursor.connection.commit()
        user_id = cursor.lastrowid
        cursor.close

        return user_id