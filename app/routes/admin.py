from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import secrets
from datetime import timedelta
import json
from app.database import get_db
from app.middleware.auth import (
    get_password_hash, 
    verify_password,
    create_access_token,
    get_current_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/register")
async def register_admin(
    username: str,
    password: str,
    email: str,
    full_name: str,
    current_admin: dict = Depends(get_current_admin)
):
    # Verificar si el administrador actual es superadmin
    if not current_admin.get('is_superadmin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los superadministradores pueden registrar nuevos administradores"
        )
    
    with get_db() as cursor:
        # Verificar si el usuario ya existe
        cursor.execute("SELECT id FROM admin_users WHERE username = %s OR email = %s", 
                      (username, email))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario o email ya está registrado"
            )
        
        # Crear el nuevo administrador
        hashed_password = get_password_hash(password)
        campaign_token = secrets.token_hex(32)
        
        cursor.execute("""
            INSERT INTO admin_users (username, email, password_hash, full_name, campaign_token)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, email, hashed_password, full_name, campaign_token))
        
        # Obtener el administrador recién creado
        cursor.execute("""
            SELECT id, username, email, full_name, is_active, is_superadmin, campaign_token
            FROM admin_users WHERE username = %s
        """, (username,))
        new_admin = cursor.fetchone()
        
        return new_admin

@router.post("/login")
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db() as cursor:
        cursor.execute("""
            SELECT id, username, password_hash, is_active, is_superadmin, campaign_token
            FROM admin_users WHERE username = %s
        """, (form_data.username,))
        admin = cursor.fetchone()
        
        if not admin or not verify_password(form_data.password, admin['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not admin['is_active']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": admin['username']},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "campaign_token": admin['campaign_token']  # Incluir el campaign_token en la respuesta
        }

@router.get("/my-loans")
async def get_my_loans(current_admin: dict = Depends(get_current_admin)):
    """Obtener todos los préstamos asociados a la campaña del administrador"""
    with get_db() as cursor:
        cursor.execute("""
            SELECT * FROM loans 
            WHERE campaign_token = %s 
            ORDER BY created_at DESC
        """, (current_admin['campaign_token'],))
        loans = cursor.fetchall()
        
        # Convertir las fechas a string para que sean JSON serializable
        for loan in loans:
            if loan.get('date_of_birth'):
                loan['date_of_birth'] = loan['date_of_birth'].isoformat()
            if loan.get('created_at'):
                loan['created_at'] = loan['created_at'].isoformat()
            if loan.get('updated_at'):
                loan['updated_at'] = loan['updated_at'].isoformat()
        
        return {
            "campaign_token": current_admin['campaign_token'],
            "total_loans": len(loans),
            "loans": loans
        }