import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='1234',
            database='hotel',
            ssl_disabled=True
        )
        if connection.is_connected():
            print('Conexión exitosa a la base de datos MySQL')
            return connection
    except Error as e:
        print(f'Error al conectar a MySQL: {e}')
        return None

def create_database_and_table(connection):
    try:
        cursor = connection.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS hotel")
        cursor.execute("USE hotel")

        # Crear la tabla de reservas si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha_ingreso DATE NOT NULL,
                fecha_salida DATE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL,
                tarjeta VARCHAR(50),
                preferencias TEXT,
                huespedes INT NOT NULL,
                tipo_habitacion VARCHAR(50) NOT NULL
            )
        """)
        print("Base de datos y tabla creadas exitosamente")
    except Error as e:
        print(f'Error al crear la base de datos o la tabla: {e}')
    finally:
        if cursor:
            cursor.close()

def guardar_reserva_en_db(fecha_ingreso, fecha_salida, nombre, telefono, email, preferencias, huespedes, tipo):
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="hotel"
        )
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO reservas (fecha_ingreso, fecha_salida, nombre, telefono, email, preferencias, huespedes, tipo_habitacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (fecha_ingreso, fecha_salida, nombre, telefono, email, preferencias, huespedes, tipo)
        cursor.execute(consulta, valores)
        conexion.commit()
    except Exception as e:
        print(f"Error al guardar la reserva: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

# Ejemplo de uso
if __name__ == '__main__':
    connection = create_connection()
    if connection:
        create_database_and_table(connection)
        connection.close()
