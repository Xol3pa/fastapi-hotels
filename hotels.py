from fastapi import APIRouter, Query, Body
from pydantic import BaseModel


hotels = [
    {'id': 1, 'title': 'Sochi', "name": "sochi"},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'}
]

class Hotel(BaseModel):
    title: str
    name: str

router = APIRouter(prefix= '/hotels', tags=['Отели'])


@router.get("")
def get_hotels(
        hotel_id: int | None = Query(None, description="Hotel ID"),
        title: str | None = Query(None, description="Hotel title"),
):
    hotels_ = []

    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels

    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })

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
        title: str | None = Body(None, embed=True, description="Hotel title"),
        name: str | None = Body(None, embed=True, description="Hotel name"),
):
    global hotels

    hotel_to_update = next((hotel for hotel in hotels if hotel['id'] == hotel_id), None)

    if not hotel_to_update:
        return {'error': 'Hotel not found'}

    if title and hotel_to_update["title"] != title:
        hotel_to_update["title"] = title
    if name and hotel_to_update["name"] != name:
        hotel_to_update["name"] = name

    return {"success": "true"}
