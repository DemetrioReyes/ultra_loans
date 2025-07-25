from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "A25bd1e23@@"
hashed_password = pwd_context.hash(password)
print(f"\nHash generado para la contraseña: {hashed_password}\n") 