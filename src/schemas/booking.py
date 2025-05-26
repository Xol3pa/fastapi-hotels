from datetime import date
from pydantic import Field

from . import BaseCreateSchema, BaseResponseSchema


class BookingCreate(BaseCreateSchema):
    """Схема для создания бронирования через API"""
    room_id: int = Field(..., description="ID комнаты")
    date_from: date = Field(..., description="Дата заезда")
    date_to: date = Field(..., description="Дата выезда")


class BookingCreateDB(BaseCreateSchema):
    """Схема для создания бронирования в БД"""
    user_id: int = Field(..., description="ID пользователя")
    room_id: int = Field(..., description="ID комнаты")
    date_from: date = Field(..., description="Дата заезда")
    date_to: date = Field(..., description="Дата выезда")
    price: int = Field(..., gt=0, description="Общая стоимость")


class Booking(BaseResponseSchema):
    """Схема бронирования для ответа"""
    user_id: int = Field(..., description="ID пользователя")
    room_id: int = Field(..., description="ID комнаты")
    date_from: date = Field(..., description="Дата заезда")
    date_to: date = Field(..., description="Дата выезда")
    price: int = Field(..., description="Общая стоимость")