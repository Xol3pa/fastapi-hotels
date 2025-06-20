import logging

from sqlalchemy import select

from src.exceptions import ObjectNotFoundException
from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.schemas.facilities import RoomFacilityCreate, Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    mapper = FacilityDataMapper

    async def get_by_ids(self, facilities_ids: list[int]) -> list[Facility]:
        if not facilities_ids:
            return []

        result = await self.get_filtered(self.model.id.in_(facilities_ids))
        if len(result) != len(facilities_ids):
            missing_ids = set(facilities_ids) - set(result)
            logging.warning(f"Facilities not found: {missing_ids}")
            raise ObjectNotFoundException

        return result


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    mapper = RoomFacilityDataMapper

    async def partially_edit(self, room_id: int, facilities_ids: list[int]):
        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        result = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids = set(result.scalars().all())
        new_facilities = set(facilities_ids)

        to_add = new_facilities - current_facilities_ids
        to_remove = current_facilities_ids - new_facilities

        if to_remove:
            await self.delete(
                self.model.facility_id.in_(list(to_remove)),
                room_id=room_id,
            )

        if to_add:
            room_facilities_data = [
                RoomFacilityCreate(room_id=room_id, facility_id=facility_id)
                for facility_id in to_add
            ]
            await self.add_bulk(data=room_facilities_data)
