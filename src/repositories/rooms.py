from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import coalesce

from src.database import engine
from src.exceptions import ObjectNotFoundException, InvalidDateRangeException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.repositories.mappers.mappers import RoomDataMapper, RoomsWithRelsDataMapper
from src.repositories.utils import rooms_booked_table_query
from src.schemas.rooms import Room, RoomCreateDB


class RoomsRepository(BaseRepository):
    model = RoomsModel
    mapper = RoomDataMapper

    async def get_all(self, *args, **kwargs) -> List[Room]:
        return await super().get_all(*args, **kwargs)

    async def get_filtered(self, *filter, **filter_by) -> List[Room]:
        return await super().get_filtered(*filter_by, **filter_by)

    async def add(self, data: RoomCreateDB) -> Optional[Room]:
        return await super().add(data)

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        if date_from >= date_to:
            raise InvalidDateRangeException

        rooms_booked_table = rooms_booked_table_query(
            date_from=date_from,
            date_to=date_to,
        )

        rooms_availability = (
            select(self.model.id)
            .select_from(self.model)
            .outerjoin(
                rooms_booked_table, self.model.id == rooms_booked_table.c.room_id
            )
            .filter(
                self.model.hotel_id == hotel_id,
                (self.model.quantity - coalesce(rooms_booked_table.c.booked_rooms, 0))
                > 0,
            )
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_availability))
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return [
            RoomsWithRelsDataMapper.map_to_domain_entity(room)
            for room in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by) -> Optional[Room]:
        query = (
            select(self.model)
            .select_from(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        return RoomsWithRelsDataMapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> Room:
        query = (
            select(self.model)
            .select_from(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return RoomsWithRelsDataMapper.map_to_domain_entity(model)
