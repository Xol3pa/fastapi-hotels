from datetime import date
from sqlalchemy import select, func
from sqlalchemy.sql.functions import coalesce

from src.database import engine
from src.models.booking import BookingModel
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
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
        WITH rooms_count AS
        (
            SELECT bookings.room_id AS room_id, count('*') AS rooms_booked
            FROM bookings
            WHERE bookings.date_from <= '2025-03-27' AND bookings.date_to >= '2025-03-23'
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
                rooms.quantity - coalesce(rooms_count.rooms_booked, 0) AS quantity
            FROM rooms
            LEFT OUTER JOIN rooms_count ON rooms.id = rooms_count.room_id
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
        """
        !WITH rooms_count AS
        (
            SELECT bookings.room_id AS room_id, count('*') AS rooms_booked
            FROM bookings
            WHERE bookings.date_from <= '2025-03-27' AND bookings.date_to >= '2025-03-23'
            GROUP BY bookings.room_id
        ),
        """
        rooms_count = (
            select(
                BookingModel.room_id,
                func.count("*").label("rooms_booked")
            )
            .select_from(BookingModel)
            .filter(
                BookingModel.date_from <= date_to,
                BookingModel.date_to >= date_from,
            )
            .group_by(BookingModel.room_id)
            .cte(name="rooms_count")
        )

        """
        !rooms_availability AS 
        (
            SELECT 
                rooms.id AS id, 
                rooms.hotel_id AS hotel_id, 
                rooms.title AS title, 
                rooms.description AS description, 
                rooms.price AS price, 
                rooms.quantity - coalesce(rooms_count.rooms_booked, 0) AS quantity 
            FROM rooms 
            LEFT OUTER JOIN rooms_count ON rooms.id = rooms_count.room_id 
            WHERE rooms.hotel_id = 20
        )
        """

        rooms_availability = (
            select(
                RoomsModel.id,
                RoomsModel.hotel_id,
                RoomsModel.title,
                RoomsModel.description,
                RoomsModel.price,
                (RoomsModel.quantity - coalesce(rooms_count.c.rooms_booked, 0)).label("quantity")
            )
            .select_from(RoomsModel)
            .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
            .filter(
                RoomsModel.hotel_id == hotel_id,
            )
            .cte(name="rooms_availability")
        )

        """
        !SELECT 
            rooms_availability.id, 
            rooms_availability.hotel_id, 
            rooms_availability.title, 
            rooms_availability.description, 
            rooms_availability.price, 
            rooms_availability.quantity 
        FROM rooms_availability 
        WHERE rooms_availability.quantity > 0
        """

        query = (
            select(rooms_availability)
            .filter(rooms_availability.c.quantity > 0)
        )

        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return [self.schema.model_validate(row) for row in result.mappings().all()]


