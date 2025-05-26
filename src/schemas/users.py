from pydantic import EmailStr, Field

from . import BaseCreateSchema, BaseResponseSchema, BaseSchema


class UserCreate(BaseCreateSchema):
    """Схема для создания пользователя через API"""
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")


class UserCreateDB(BaseCreateSchema):
    """Схема для создания пользователя в БД"""
    email: EmailStr = Field(..., description="Email пользователя")
    hashed_password: str = Field(..., description="Хешированный пароль")


class User(BaseResponseSchema):
    """Схема пользователя для ответа"""
    email: EmailStr = Field(..., description="Email пользователя")


class UserWithPassword(User):
    """Схема пользователя с паролем для внутреннего использования"""
    hashed_password: str = Field(..., description="Хешированный пароль")