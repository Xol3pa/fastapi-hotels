from typing import Optional
from pydantic import Field

from . import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class HotelCreate(BaseCreateSchema):
    """Схема для создания отеля"""

    title: str = Field(..., description="Название отеля")
    location: str = Field(..., description="Местоположение отеля")


class HotelUpdate(BaseUpdateSchema):
    """Схема для обновления отеля"""

    title: Optional[str] = Field(None, description="Название отеля")
    location: Optional[str] = Field(None, description="Местоположение отеля")


class Hotel(BaseResponseSchema):
    """Схема отеля для ответа"""

    title: str = Field(..., description="Название отеля")
    location: str = Field(..., description="Местоположение отеля")
