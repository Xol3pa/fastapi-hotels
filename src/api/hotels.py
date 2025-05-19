from fastapi import APIRouter, Query
import math

from sqlalchemy import insert, select
from src.database import async_session_maker, engine
from src.models.hotels import HotelsModel
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
        query = select(HotelsModel)
        if location:
            query = query.where(HotelsModel.location.ilike(f'%{location}%'))
        if title:
            query = query.where(HotelsModel.title.ilike(f'%{title}%'))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)

        return result.scalars().all()

@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {
        "success": "true",
    }

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"success": "true"}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    hotel_to_update = next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    if not hotel_to_update:
        return {'error': 'Hotel not found'}

    hotel_to_update["title"] = hotel_data.title
    hotel_to_update["name"] = hotel_data.name

    return {"success": "true"}

@router.patch("/{hotel_id}")
def change_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels

    hotel_to_update = next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    if not hotel_to_update:
        return {'error': 'Hotel not found'}

    if hotel_data.title and hotel_to_update["title"] != hotel_data.title:
        hotel_to_update["title"] = hotel_data.title
    if hotel_data.name and hotel_to_update["name"] != hotel_data.name:
        hotel_to_update["name"] = hotel_data.name

    return {"success": "true"}
