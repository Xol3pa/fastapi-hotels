from datetime import date
from typing import Optional

from src.database import engine
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from sqlalchemy import select, func

from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_booked_table_query
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper = HotelDataMapper

    async def get_filtered(
        self,
        date_from: date,
        date_to: date,
        location: Optional[str],
        title: Optional[str],
        limit: Optional[int],
        offset: Optional[int],
    ) -> list[Hotel]:
        """
        WITH rooms_booked_table AS (
            select bookings.room_id, count(*) as booked_rooms
            from bookings
            where bookings.date_from <= '2025-01-03' and bookings.date_to >= '2025-01-01'
            group by bookings.room_id
        )
        SELECT
            hotels.id,
            hotels.title,
            hotels.location
        FROM hotels
        WHERE hotels.id IN (
            SELECT
                rooms.hotel_id
            FROM rooms
            LEFT OUTER JOIN rooms_booked_table ON rooms.id = rooms_booked_table.room_id
            WHERE rooms.quantity - coalesce(rooms_booked_table.booked_rooms, 0) > 0
        )
        """

        rooms_booked_table = rooms_booked_table_query(
            date_from=date_from,
            date_to=date_to,
        )

        available_rooms = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .outerjoin(
                rooms_booked_table, RoomsModel.id == rooms_booked_table.c.room_id
            )
            .filter(
                (
                    RoomsModel.quantity
                    - func.coalesce(rooms_booked_table.c.booked_rooms, 0)
                )
                > 0
            )
        )

        query = (
            select(
                HotelsModel.id,
                HotelsModel.title,
                HotelsModel.location,
            )
            .select_from(HotelsModel)
            .filter(HotelsModel.id.in_(available_rooms))
        )

        if location:
            query = query.filter(
                func.lower(HotelsModel.location).contains(func.lower(location))
            )
        if title:
            query = query.filter(
                func.lower(HotelsModel.title).contains(func.lower(title))
            )

        query = query.limit(limit).offset(offset)

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)

        return [
            self.mapper.map_to_domain_entity(model) for model in result.mappings().all()
        ]
