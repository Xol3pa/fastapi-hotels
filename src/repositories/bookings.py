from datetime import date
from sqlalchemy import select

from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

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