from datetime import date
from typing import Optional

from sqlalchemy import select, func

from src.exceptions import RoomsAreOccupiedException
from src.models import RoomsModel
from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_booked_table_query
from src.schemas.booking import Booking, BookingCreateDB


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def get_all(self, *args, **kwargs) -> list[Booking]:
        return await super().get_all(*args, **kwargs)

    async def get_one_or_none(self, **filter_by) -> Optional[Booking]:
        return await super().get_one_or_none(**filter_by)

    async def get_filtered(self, *filter, **filter_by) -> list[Booking]:
        return await super().get_filtered(*filter, **filter_by)

    async def create_booking(self, data: BookingCreateDB) -> Booking:
        available_rooms = await self.check_availability(
            room_id=data.room_id, date_from=data.date_from, date_to=data.date_to
        )
        if not available_rooms:
            raise RoomsAreOccupiedException

        booking = await self.add(data)

        return booking

    async def check_availability(
        self,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_booked_table = rooms_booked_table_query(
            date_from=date_from,
            date_to=date_to,
        )

        query = (
            select(1)
            .select_from(RoomsModel)
            .outerjoin(
                rooms_booked_table, RoomsModel.id == rooms_booked_table.c.room_id
            )
            .where(
                RoomsModel.id == room_id,
                RoomsModel.quantity
                - func.coalesce(rooms_booked_table.c.booked_rooms, 0)
                > 0,
            )
        )

        result = await self.session.execute(query)
        return result.scalar() is not None

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsModel).filter(BookingsModel.date_from <= date.today())
        res = await self.session.execute(query)

        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]
