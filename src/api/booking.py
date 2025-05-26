from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.models.bookings import BookingsModel
from src.schemas.booking import BookingCreate, BookingCreateDB

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.get("")
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
async def create_booking(
        db: DBDep,
        booking_data: BookingCreate,
        user_id: UserIdDep
):
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room_data is None:
        raise HTTPException(status_code=404, detail="Room not found")

    overlapping_booking = await db.bookings.check_overlap(
        room_id=room_data.id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
    )

    if overlapping_booking:
        raise HTTPException(status_code=409, detail="Room is already booked for these dates")


    booking_price = BookingsModel(
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room_data.price
    ).total_cost

    booking = await db.bookings.add(BookingCreateDB(
        user_id=user_id,
        price=booking_price,
        **booking_data.model_dump()
    ))
    
    await db.commit()
    return {"success": True, "data": booking}

