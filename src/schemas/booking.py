from datetime import date
from typing import Optional

from pydantic import Field

from . import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


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


class BookingUpdateDB(BaseUpdateSchema):
    user_id: Optional[int] = Field(None, description="ID пользователя")
    room_id: Optional[int] = Field(None, description="ID комнаты")
    date_from: Optional[date] = Field(None, description="Дата заезда")
    date_to: Optional[date] = Field(None, description="Дата выезда")
    price: Optional[int] = Field(None, gt=0, description="Общая стоимость")


class Booking(BaseResponseSchema):
    """Схема бронирования для ответа"""

    user_id: int = Field(..., description="ID пользователя")
    room_id: int = Field(..., description="ID комнаты")
    date_from: date = Field(..., description="Дата заезда")
    date_to: date = Field(..., description="Дата выезда")
    price: int = Field(..., description="Общая стоимость")
