from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, Room, RoomAddWithHotelId

router = APIRouter(prefix='/hotels', tags=['Комнаты'])

@router.get('/{hotel_id}/rooms')
async def get_rooms(
        db: DBDep,
        hotel_id: int
) -> list[Room]:
    hotel_rooms = await db.rooms.get_all(hotel_id=hotel_id)
    return hotel_rooms


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room_by_id(
        db: DBDep,
        room_id: int,
        hotel_id: int,
):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post('/{hotel_id}/rooms')
async def create_room(
        db: DBDep,
        hotel_id: int,
        data: RoomAdd,
):
    room_data = RoomAddWithHotelId(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    room = await db.rooms.add(room_data)
    await db.commit()

    return {"data": room}

@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_change_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomPatch
):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    await db.rooms.edit(data=data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"success": True}


@router.put('/{hotel_id}/rooms/{room_id}')
async def change_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomAdd
):
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    await db.rooms.edit(data=data, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"success": True}

@router.delete('/{hotel_id}/rooms/{room_id}')
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