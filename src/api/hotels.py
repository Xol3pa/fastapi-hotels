from fastapi import APIRouter, Query, HTTPException

from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("")
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel location"),
        title: str | None = Query(None, description="Hotel title"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )

@router.get('/{hotel_id}')
async def get_hotel_by_id(
        db: DBDep,
        hotel_id: int
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404)

    return hotel

@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {
        "success": "true", 'data': hotel
    }

@router.delete("/{hotel_id}")
async def delete_hotel(
        db: DBDep,
        hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"success": "true"}


@router.put("/{hotel_id}")
async def update_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"success": "true"}

@router.patch("/{hotel_id}")
async def partially_change_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"success": "true"}
