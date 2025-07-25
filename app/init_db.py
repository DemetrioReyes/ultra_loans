from database import init_db, get_db
from middleware.auth import get_password_hash
import secrets

def create_superadmin():
    """Crea un superadmin inicial si no existe"""
    with get_db() as cursor:
        # Verificar si ya existe un superadmin
        cursor.execute("SELECT id FROM admin_users WHERE is_superadmin = TRUE")
        if cursor.fetchone():
            print("El superadmin ya existe")
            return
        
        # Crear superadmin inicial
        superadmin = {
            "username": "superadmin",
            "email": "admin@ultraloans.com",
            "password_hash": get_password_hash("admin123"),  # Cambiar esta contraseña en producción
            "full_name": "Super Administrator",
            "is_active": True,
            "is_superadmin": True,
            "campaign_token": secrets.token_hex(32)
        }
        
        cursor.execute("""
            INSERT INTO admin_users 
            (username, email, password_hash, full_name, is_active, is_superadmin, campaign_token)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            superadmin["username"],
            superadmin["email"],
            superadmin["password_hash"],
            superadmin["full_name"],
            superadmin["is_active"],
            superadmin["is_superadmin"],
            superadmin["campaign_token"]
        ))
        print("Superadmin creado exitosamente")

if __name__ == "__main__":
    print("Inicializando la base de datos...")
    init_db()
    print("Creando superadmin...")
    create_superadmin()
    print("Inicialización completada") 