from typing import Optional
from pydantic import Field

from . import BaseCreateSchema, BaseResponseSchema, BaseUpdateSchema


class RoomCreate(BaseCreateSchema):
    """Схема для создания комнаты"""
    title: str = Field(..., description="Название комнаты")
    price: int = Field(..., gt=0, description="Цена за ночь")
    quantity: int = Field(..., gt=0, description="Количество комнат")
    description: Optional[str] = Field(None, description="Описание комнаты")
    facilities_ids: list[int] = Field([], description="Список ID удобств")


class RoomCreateDB(BaseCreateSchema):
    title: str = Field(..., description="Название комнаты")
    price: int = Field(..., gt=0, description="Цена за ночь")
    quantity: int = Field(..., gt=0, description="Количество комнат")
    description: Optional[str] = Field(None, description="Описание комнаты")


class RoomCreateWithHotel(RoomCreateDB):
    """Схема для создания комнаты с привязкой к отелю для БД"""
    hotel_id: int = Field(..., description="ID отеля")


class RoomUpdateDB(BaseUpdateSchema):
    """Схема для обновления комнаты"""
    title: Optional[str] = Field(None, description="Название комнаты")
    price: Optional[int] = Field(None, gt=0, description="Цена за ночь")
    quantity: Optional[int] = Field(None, gt=0, description="Количество комнат")
    description: Optional[str] = Field(None, description="Описание комнаты")


class RoomUpdate(RoomUpdateDB):
    facilities_ids: list[int] = Field([], description="Список ID удобств")


class Room(BaseResponseSchema):
    """Схема комнаты для ответа"""
    hotel_id: int = Field(..., description="ID отеля")
    title: str = Field(..., description="Название комнаты")
    price: int = Field(..., description="Цена за ночь")
    quantity: int = Field(..., description="Количество комнат")
    description: str = Field(..., description="Описание комнаты")