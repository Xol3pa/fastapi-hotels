from datetime import date
from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.exceptions import (
    ObjectNotFoundException,
    check_date_to_after_date_from,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import HotelUpdate, HotelCreate
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    date_from: date = Query(examples=["2025-05-01"]),
    date_to: date = Query(examples=["2025-05-02"]),
    location: str | None = Query(None, description="Hotel location"),
    title: str | None = Query(None, description="Hotel title"),
):
    check_date_to_after_date_from(date_from, date_to)

    per_page = pagination.per_page or 5
    hotels = await db.hotels.get_filtered(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )

    return hotels


@router.get("/{hotel_id}")
async def get_hotel_by_id(db: DBDep, hotel_id: int):
    try:
        hotel = await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    return hotel


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelCreate):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"success": "true", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelCreate):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"success": "true"}


@router.patch("/{hotel_id}")
async def partially_change_hotel(db: DBDep, hotel_id: int, hotel_data: HotelUpdate):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"success": "true"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"success": "true"}
