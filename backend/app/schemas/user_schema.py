# backend/app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес")
    full_name: Optional[str] = Field(None, max_length=200, description="Полное имя")
    phone: Optional[str] = Field(None, max_length=20, description="Номер телефона")
    
    @validator('username')
    def validate_username(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username может содержать только буквы, цифры и _')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, description="Пароль")


class UserLogin(BaseModel):
    username: str = Field(..., description="Имя пользователя")
    password: str = Field(..., description="Пароль")


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    hashed_password: str
    
    class Config:
        from_attributes = True
        