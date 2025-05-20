from fastapi import APIRouter, Query
from repositories.hotels import HotelsRepository
from src.database import async_session_maker, engine
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep


router = APIRouter(prefix= '/hotels', tags=['Отели'])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel location"),
        title: str | None = Query(None, description="Hotel title"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    print(type(hotel), hotel)

    return {
        "success": "true", 'data': hotel
    }

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"success": "true"}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"success": "true"}

@router.patch("/{hotel_id}")
async def partially_change_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"success": "true"}
