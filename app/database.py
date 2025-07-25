import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@contextmanager
def get_db():
    conn = get_db_connection()
    if conn is None:
        raise Exception("No se pudo conectar a la base de datos")
    try:
        cursor = conn.cursor(dictionary=True)
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def init_db():
    """Inicializa las tablas de la base de datos"""
    conn = get_db_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        # Crear tabla de administradores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                is_superadmin BOOLEAN DEFAULT FALSE,
                campaign_token VARCHAR(64) UNIQUE
            )
        """)
        conn.commit()
        print("Tablas creadas exitosamente")
    except Error as e:
        print(f"Error creando tablas: {e}")
    finally:
        cursor.close()
        conn.close()