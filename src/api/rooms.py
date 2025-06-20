from datetime import date
from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException, RoomNotFoundException, InvalidDateRangeException, InvalidDateRangeHTTPException,
    HotelNotFoundException, FacilityNotFoundException, FacilityNotFoundHTTPException,
)
from src.schemas.rooms import (
    RoomCreate,
    RoomUpdate,
    RoomWithRels,
)
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2025-05-01"]),
    date_to: date = Query(examples=["2025-05-02"]),
) -> list[RoomWithRels]:
    """Получение всех комнат отеля"""

    try:
        hotel_rooms =  await RoomsService(db).get_rooms(hotel_id, date_from, date_to)
    except InvalidDateRangeException:
        raise InvalidDateRangeHTTPException
    return hotel_rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    db: DBDep,
    room_id: int,
    hotel_id: int,
):
    """Получение комнаты"""

    try:
        room = await RoomsService(db).get_room_by_id(room_id, hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return room


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomCreate,
):
    """Создание комнаты"""

    try:
        room = await RoomsService(db).create_room(hotel_id, data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return {"data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(db: DBDep, hotel_id: int, room_id: int, data: RoomCreate):
    """Изменение данных комнаты"""

    try:
        await RoomsService(db).change_room(hotel_id, room_id, data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException

    return {"success": True}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_change_room(
    db: DBDep, hotel_id: int, room_id: int, data: RoomUpdate
):
    """Частичное изменение данных комнаты"""

    try:
        await RoomsService(db).partially_change_room(hotel_id, room_id, data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException

    return {"success": True}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    """Удаление комнаты"""

    try:
        await RoomsService(db).delete_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"success": True}
