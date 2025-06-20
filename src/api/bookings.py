from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    RoomsAreOccupiedException,
    RoomNotFoundHTTPException,
    RoomsAreOccupiedHTTPException,
    RoomNotFoundException,
)
from src.schemas.booking import BookingCreate
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
@cache(expire=10)
async def get_all_bookings(
    db: DBDep,
):
    """Получение всех бронирований"""

    return BookingsService(db).get_all_bookings()


@router.get("/me")
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    """Получение бронирований определенного пользователя"""

    return await BookingsService(db).get_user_bookings(user_id)


@router.post("")
async def create_booking(db: DBDep, booking_data: BookingCreate, user_id: UserIdDep):
    """Создание бронирования"""

    try:
        booking = await BookingsService(db).create_booking(booking_data, user_id)
    except RoomsAreOccupiedException:
        raise RoomsAreOccupiedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"success": True, "data": booking}
