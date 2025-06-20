from typing import Optional

from src.exceptions import RoomsAreOccupiedException, BookingsNotFoundException
from src.models import BookingsModel
from src.schemas.booking import BookingCreate, BookingCreateDB, Booking
from src.services.base import BaseService


class BookingsService(BaseService):
    """Сервисный слой для работы с эндопинтами /bookings"""

    async def get_all_bookings(self) -> Optional[list[Booking]]:
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: int) -> Optional[list[Booking]]:
        bookings = await self.db.bookings.get_user_bookings(user_id)
        if not bookings:
            raise BookingsNotFoundException

        return bookings

    async def create_booking(self, data: BookingCreate, user_id: int) -> Booking:
        self.date_validator.validate_date_to_after_date_from(
            data.date_from, data.date_to
        )
        room_data = await self.entity_validator.validate_room_exists_any_hotel(
            room_id=data.room_id
        )
        booking_price = BookingsModel(
            date_from=data.date_from,
            date_to=data.date_to,
            price=room_data.price,
        ).total_cost

        try:
            booking = await self.db.bookings.create_booking(
                BookingCreateDB(
                    user_id=user_id, price=booking_price, **data.model_dump()
                )
            )
        except RoomsAreOccupiedException:
            raise RoomsAreOccupiedException

        await self.db.commit()

        return booking
