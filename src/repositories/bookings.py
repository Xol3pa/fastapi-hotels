from datetime import date
from typing import List, Optional

from sqlalchemy import select

from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.booking import Booking, BookingCreateDB


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def get_all(self, *args, **kwargs) -> List[Booking]:
        return await super().get_all(*args, **kwargs)

    async def get_one_or_none(self, **filter_by) -> Optional[Booking]:
        return await super().get_one_or_none(**filter_by)

    async def get_filtered(self, *filter, **filter_by) -> List[Booking]:
        return await super().get_filtered(*filter_by, **filter_by)

    async def add(self, data: BookingCreateDB) -> Optional[Booking]:
        return await super().add(data)

    async def check_overlap(
            self,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        query = select(self.model).where(
            self.model.room_id == room_id,
            self.model.date_from <= date_to,
            self.model.date_to >= date_from,
        )

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None

        return self.mapper.map_to_domain_entity(model)

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsModel)
            .filter(BookingsModel.date_from <= date.today())
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]