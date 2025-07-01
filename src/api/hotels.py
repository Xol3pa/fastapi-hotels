from datetime import date
from fastapi import APIRouter, Query
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from src.exceptions import (
    HotelNotFoundHTTPException,
    InvalidDeleteOptionsException,
    InvalidDeleteOptionsHTTPException,
    InvalidDateRangeException,
    InvalidDateRangeHTTPException,
    HotelNotFoundException,
)
from src.schemas.hotels import HotelUpdate, HotelCreate, Hotel
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelsService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=60)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(openapi_examples={
        "current": Example(value=date(2020, 1, 1))
    }),
    date_to: date = Query(openapi_examples={
        "future": Example(value=date(2020, 1, 5))
    }),
    location: str | None = Query(None, description="Hotel location"),
    title: str | None = Query(None, description="Hotel title"),
) -> list[Hotel]:
    """Получение всех отелей по фильтрам"""

    try:
        hotels = await HotelsService(db).get_hotels(
            pagination, date_from, date_to, location, title
        )
    except InvalidDateRangeException:
        raise InvalidDateRangeHTTPException
    return hotels


@router.get("/{hotel_id}")
async def get_hotel_by_id(db: DBDep, hotel_id: int) -> Hotel:
    """Получение определенного отеля"""

    try:
        hotel = await HotelsService(db).get_hotel_by_id(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return hotel


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelCreate):
    """Создание отеля"""

    hotel = await HotelsService(db).create_hotel(hotel_data)
    return {"success": True, "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelCreate):
    """Полное обновление данных отеля"""

    try:
        await HotelsService(db).update_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"success": True}


@router.patch("/{hotel_id}")
async def partially_change_hotel(db: DBDep, hotel_id: int, hotel_data: HotelUpdate):
    """Частичное обновление данных отеля"""

    try:
        await HotelsService(db).partially_change_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"success": True}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    """Удаление отеля"""

    try:
        await HotelsService(db).delete_hotel(hotel_id)
    except InvalidDeleteOptionsException:
        raise InvalidDeleteOptionsHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"success": True}
