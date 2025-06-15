from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, RoomsAreOccupiedException
from src.models.bookings import BookingsModel
from src.schemas.booking import BookingCreate, BookingCreateDB

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
@cache(expire=10)
async def get_all_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(db: DBDep, booking_data: BookingCreate, user_id: UserIdDep):
    try:
        room_data = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Room not found")

    booking_price = BookingsModel(
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room_data.price,
    ).total_cost

    try:
        booking = await db.bookings.create_booking(
            BookingCreateDB(
                user_id=user_id, price=booking_price, **booking_data.model_dump()
            )
        )
    except RoomsAreOccupiedException as e:
        raise HTTPException(status_code=409, detail=e.detail)

    await db.commit()
    return {"success": True, "data": booking}
