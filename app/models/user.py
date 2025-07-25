from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superadmin = Column(Boolean, default=False)
    campaign_token = Column(String(64), unique=True)  # Token único para cada campaña