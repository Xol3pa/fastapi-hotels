from datetime import date
from typing import Optional

from src.api.dependencies import PaginationParams
from src.schemas.hotels import HotelCreate, HotelUpdate
from src.services.base import BaseService


class HotelsService(BaseService):
    """Сервисный слой для работы с эндпоинтами /hotels"""

    async def get_hotels(
        self,
        pagination: PaginationParams,
        date_from: date,
        date_to: date,
        location: Optional[str],
        title: Optional[str],
    ):
        self.date_validator.validate_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        hotels = await self.db.hotels.get_filtered(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

        return hotels

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.entity_validator.validate_hotel_exists(hotel_id)

    async def create_hotel(self, hotel_data: HotelCreate):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()

        return hotel

    async def update_hotel(self, hotel_id: int, hotel_data: HotelCreate):
        await self.entity_validator.validate_hotel_exists(hotel_id)
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def partially_change_hotel(self, hotel_id: int, hotel_data: HotelUpdate):
        await self.entity_validator.validate_hotel_exists(hotel_id)
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.entity_validator.validate_hotel_exists(hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
