from app import mysql

class imgModel:
    def obtener_img(self, id):
        cursor = mysql.connection.cursor()
        sql = "SELECT nomArchivo FROM imagenes where producto = %s"
        cursor.execute(sql, (id,))
        imagenes = cursor.fetchall()
        cursor.close()

        return imagenes
    
    def cargar_img(self, id, archivos):
        cursor = mysql.connection.cursor()
        mysql.connection.begin()
        sql = "INSERT INTO imagenes (producto, nomArchivo) VALUES (%s, %s)"

        try:
            for a in archivos:
                cursor.execute(sql, (id, a))
            

            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            print(str(e))
            return 0

        cant = cursor.rowcount
        cursor.close()
        
        return cant