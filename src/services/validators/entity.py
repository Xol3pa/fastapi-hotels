from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    HotelNotFoundException,
    FacilityNotFoundException,
    UserNotFoundException,
)
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.rooms import RoomWithRels
from src.schemas.users import User
from src.services.validators.base import BaseValidator


class EntityValidator(BaseValidator):
    """Валидация существования сущностей"""

    async def validate_room_exists(self, room_id: int, hotel_id: int) -> RoomWithRels:
        try:
            room = await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        return room

    async def validate_room_exists_any_hotel(self, room_id: int) -> RoomWithRels:
        """Поиск комнаты не зная отеля"""
        try:
            room = await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        return room

    async def validate_hotel_exists(self, hotel_id: int) -> Hotel:
        try:
            hotel = await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        return hotel

    async def validate_facilities_exist(
        self, facilities_ids: list[int]
    ) -> list[Facility]:
        if not facilities_ids:
            return []

        try:
            facilities = await self.db.facilities.get_by_ids(facilities_ids)
        except ObjectNotFoundException:
            raise FacilityNotFoundException
        return facilities

    async def validate_user_exists(self, **filter_by) -> User:
        try:
            user = await self.db.users.get_one(**filter_by)
        except ObjectNotFoundException:
            raise UserNotFoundException
        return user
