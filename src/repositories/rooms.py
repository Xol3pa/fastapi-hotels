from datetime import date
from sqlalchemy import select
from sqlalchemy.sql.functions import coalesce

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.repositories.utils import rooms_booked_table_query
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH rooms_booked_table AS
        (
            SELECT
                bookings.room_id AS room_id,
                count('*') AS booked_rooms
            FROM bookings
            WHERE bookings.date_from <= '2025-05-01' AND bookings.date_to >= '2025-05-01'
            GROUP BY bookings.room_id
        ),
        rooms_availability AS
        (
            SELECT
                rooms.id AS id,
                rooms.hotel_id AS hotel_id,
                rooms.title AS title,
                rooms.description AS description,
                rooms.price AS price,
                rooms.quantity - coalesce(rooms_booked_table.booked_rooms, 0) AS quantity
            FROM rooms
            LEFT OUTER JOIN rooms_booked_table ON rooms.id = rooms_booked_table.room_id
            WHERE rooms.hotel_id = 20
        )
        SELECT
            rooms_availability.id,
            rooms_availability.hotel_id,
            rooms_availability.title,
            rooms_availability.description,
            rooms_availability.price,
            rooms_availability.quantity
        FROM rooms_availability
        WHERE rooms_availability.quantity > 0
        """

        rooms_booked_table = rooms_booked_table_query(
            date_from=date_from,
            date_to=date_to,
        )

        rooms_availability = (
            select(
                RoomsModel.id,
                RoomsModel.hotel_id,
                RoomsModel.title,
                RoomsModel.description,
                RoomsModel.price,
                (RoomsModel.quantity - coalesce(rooms_booked_table.c.booked_rooms, 0)).label("quantity")
            )
            .select_from(RoomsModel)
            .outerjoin(rooms_booked_table, RoomsModel.id == rooms_booked_table.c.room_id)
            .filter(
                RoomsModel.hotel_id == hotel_id,
            )
            .cte(name="rooms_availability")
        )

        query = (
            select(rooms_availability)
            .filter(rooms_availability.c.quantity > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return [self.schema.model_validate(row) for row in result.mappings().all()]


