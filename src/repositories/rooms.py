from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import coalesce

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.repositories.mappers.mappers import RoomDataMapper, RoomsWithRelsDataMapper
from src.repositories.utils import rooms_booked_table_query
from src.schemas.rooms import Room, RoomsWithRels


class RoomsRepository(BaseRepository):
    model = RoomsModel
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        rooms_booked_table = rooms_booked_table_query(
            date_from=date_from,
            date_to=date_to,
        )

        rooms_availability = (
            select(self.model.id)
            .select_from(self.model)
            .outerjoin(rooms_booked_table, self.model.id == rooms_booked_table.c.room_id)
            .filter(
                self.model.hotel_id == hotel_id,
                (self.model.quantity - coalesce(rooms_booked_table.c.booked_rooms, 0)) > 0
            )
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_availability))
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return [RoomsWithRelsDataMapper.map_to_domain_entity(room) for room in result.scalars().all()]

    async def get_one_or_none(
            self,
            **filter_by
    ):
        query = (
            select(self.model)
            .select_from(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        return RoomsWithRelsDataMapper.map_to_domain_entity(model)