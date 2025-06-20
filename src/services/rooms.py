from datetime import date

from src.schemas.facilities import RoomFacilityCreate
from src.schemas.rooms import (
    RoomWithRels,
    RoomCreate,
    RoomCreateWithHotel,
    RoomCreateDB,
    RoomUpdate,
    RoomUpdateDB,
)
from src.services.base import BaseService


class RoomsService(BaseService):
    """Сервисный слой для работы с эндпоинтами /hotels/{hotel_id}/rooms"""

    async def get_rooms(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ) -> list[RoomWithRels]:
        self.date_validator.validate_date_to_after_date_from(date_from, date_to)
        hotel_rooms = await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
        return hotel_rooms

    async def get_room_by_id(self, room_id: int, hotel_id: int) -> RoomWithRels:
        return await self.entity_validator.validate_room_exists(
            room_id=room_id, hotel_id=hotel_id
        )

    async def create_room(self, hotel_id: int, data: RoomCreate) -> RoomWithRels:
        await self.entity_validator.validate_hotel_exists(hotel_id=hotel_id)

        facilities = []
        if data.facilities_ids:
            facilities = await self.entity_validator.validate_facilities_exist(
                data.facilities_ids
            )

        room_data = RoomCreateWithHotel(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.add(room_data)

        if data.facilities_ids:
            room_facilities_data = [
                RoomFacilityCreate(room_id=room.id, facility_id=facility_id)
                for facility_id in data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(room_facilities_data)

        room: RoomWithRels = RoomWithRels(**room.model_dump(), facilities=facilities)
        await self.db.commit()
        return room

    async def change_room(self, hotel_id: int, room_id: int, data: RoomCreate) -> None:
        await self.entity_validator.validate_room_exists(
            room_id=room_id, hotel_id=hotel_id
        )

        if data.facilities_ids:
            await self.entity_validator.validate_facilities_exist(data.facilities_ids)

        new_room_data = RoomCreateDB(**data.model_dump())

        await self.db.rooms.edit(data=new_room_data, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.partially_edit(
            room_id=room_id,
            facilities_ids=data.facilities_ids,
        )
        await self.db.commit()

    async def partially_change_room(
        self, hotel_id: int, room_id: int, data: RoomUpdate
    ) -> None:
        await self.entity_validator.validate_room_exists(
            room_id=room_id, hotel_id=hotel_id
        )

        room_data = RoomUpdateDB(**data.model_dump(exclude_unset=True))

        if room_data.model_dump(exclude_unset=True):
            await self.db.rooms.edit(
                data=room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
            )

        if data.facilities_ids is not None:
            if data.facilities_ids:
                await self.entity_validator.validate_facilities_exist(
                    data.facilities_ids
                )

            await self.db.rooms_facilities.partially_edit(
                room_id=room_id,
                facilities_ids=data.facilities_ids,
            )

        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int) -> None:
        await self.entity_validator.validate_room_exists(
            room_id=room_id, hotel_id=hotel_id
        )
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
