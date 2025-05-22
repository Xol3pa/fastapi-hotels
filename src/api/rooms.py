from fastapi import APIRouter, HTTPException

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH, Room, RoomAddWithHotelId

router = APIRouter(prefix='/hotels', tags=['Комнаты'])

@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int) -> list[Room]:
    async with async_session_maker() as session:
        hotel_rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
        return hotel_rooms


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room_by_id(
        room_id: int,
        hotel_id: int,
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room


@router.post('/{hotel_id}/rooms')
async def create_room(
        hotel_id: int,
        data: RoomAdd,
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        room_data = data.model_dump()
        room_data["hotel_id"] = hotel_id
        room = await RoomsRepository(session).add(RoomAddWithHotelId(**room_data))
        await session.commit()

        return {"data": room}

@router.patch('/{hotel_id}/rooms/{room_id}')
async def partially_change_room(
    hotel_id: int,
    room_id: int,
    data: RoomPATCH
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        await RoomsRepository(session).edit(data=data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"success": True}


@router.put('/{hotel_id}/rooms/{room_id}')
async def change_room(
        hotel_id: int,
        room_id: int,
        data: RoomAdd
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        await RoomsRepository(session).edit(data=data, id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"success": True}

@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"success": True}