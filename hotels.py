from fastapi import APIRouter, Query
import math
from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep

hotels = [
    {'id': 1, 'title': 'Sochi', "name": "sochi"},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
    {'id': 3, 'title': 'Moscow', 'name': 'moscow'},
    {'id': 4, 'title': 'New York', 'name': 'new york'},
    {'id': 5, 'title': 'London', 'name': 'london'},
    {'id': 6, 'title': 'Paris', 'name': 'paris'},
    {'id': 7, 'title': 'Rome', 'name': 'rome'},
]

router = APIRouter(prefix= '/hotels', tags=['Отели'])


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        hotel_id: int | None = Query(None, description="Hotel ID"),
        title: str | None = Query(None, description="Hotel title"),
):
    filtered_hotels = []
    for hotel in hotels:
        if hotel_id and hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title:
            continue
        filtered_hotels.append(hotel)

    total_pages = math.ceil(len(filtered_hotels) / pagination.per_page)

    if pagination.page > total_pages and filtered_hotels:
        return {'error': 'Page not found'}

    return {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total_hotels': len(filtered_hotels),
        'total_pages': total_pages,
        'data': filtered_hotels[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]
    }

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
