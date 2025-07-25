from pydantic import BaseModel, EmailStr

class AdminBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int
    is_active: bool
    is_superadmin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None 