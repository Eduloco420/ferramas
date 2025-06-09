from app import mysql

class imgModel:
    def obtener_img(self, id):
        cursor = mysql.connection.cursor()
        sql = "SELECT nomArchivo FROM imagenes where producto = %s"
        cursor.execute(sql, (id,))
        imagenes = cursor.fetchall()
        cursor.close()

        return imagenes
    
    def cargar_img(self, id, nomArchivo):
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO imagenes (producto, nomArchivo) VALUES (%s, %s)"
        cursor.execute(sql, (id, nomArchivo))
        cursor.close()

        
