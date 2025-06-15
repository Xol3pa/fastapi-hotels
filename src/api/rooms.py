from datetime import date
from fastapi import APIRouter, HTTPException, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityCreate
from src.schemas.rooms import (
    RoomCreate,
    RoomUpdate,
    RoomCreateWithHotel,
    RoomCreateDB,
    RoomUpdateDB,
    RoomsWithRels,
)

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
@cache(expire=10)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2025-05-01"]),
    date_to: date = Query(examples=["2025-05-01"]),
) -> list[RoomsWithRels]:
    hotel_rooms = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )
    return hotel_rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room_by_id(
    db: DBDep,
    room_id: int,
    hotel_id: int,
) -> RoomsWithRels:
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    data: RoomCreate,
):
    room_data = RoomCreateWithHotel(hotel_id=hotel_id, **data.model_dump())
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")

    room = await db.rooms.add(room_data)

    if data.facilities_ids:
        room_facilities_data = [
            RoomFacilityCreate(room_id=room.id, facility_id=facility_id)
            for facility_id in data.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(room_facilities_data)

    await db.commit()

    return {"data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(db: DBDep, hotel_id: int, room_id: int, data: RoomCreate):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    new_room_data = RoomCreateDB(**data.model_dump())

    await db.rooms.edit(data=new_room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.partially_edit(
        room_id=room_id,
        data=data.facilities_ids,
    )
    await db.commit()

    return {"success": True}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_change_room(
    db: DBDep, hotel_id: int, room_id: int, data: RoomUpdate
):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    room_data = RoomUpdateDB(**data.model_dump(exclude_unset=True))

    if room_data:
        await db.rooms.edit(
            data=room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )

    if data.facilities_ids:
        await db.rooms_facilities.partially_edit(
            room_id=room_id,
            data=data.facilities_ids,
        )

    await db.commit()

    return {"success": True}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"success": True}
