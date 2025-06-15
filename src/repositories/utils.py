from datetime import date
from sqlalchemy import select, func

from src.models.bookings import BookingsModel


def rooms_booked_table_query(
    date_from: date,
    date_to: date,
):
    """
    with rooms_booked_table as (
        select bookings.room_id, count(*) as booked_rooms
        from bookings
        where bookings.date_from <= '2025-01-03' and bookings.date_to >= '2025-01-01'
        group by bookings.room_id
    )
    """

    return (
        select(BookingsModel.room_id, func.count("*").label("booked_rooms"))
        .select_from(BookingsModel)
        .filter(
            BookingsModel.date_from <= date_to,
            BookingsModel.date_to >= date_from,
        )
        .group_by(BookingsModel.room_id)
        .cte(name="rooms_booked_table")
    )
