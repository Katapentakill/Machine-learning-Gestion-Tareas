import sqlite3

def test_connection():
    test_db_path = r"D:\\Ale\\Recomend System\\Port-backend-nestjs\\test_database.sqlite"
    try:
        conn = sqlite3.connect(test_db_path)
        print("Conexión exitosa a la base de datos de prueba.")
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos de prueba: {e}")

test_connection()