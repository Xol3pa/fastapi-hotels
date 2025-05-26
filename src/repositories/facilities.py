from src.models.facilities import Facilities, RoomsFacilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityCreate


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacility

    async def partially_edit(
            self,
            room_id: int,
            data: list[int]
    ):
        current_facilities = await self.get_filtered(room_id=room_id)
        current_facilities_ids = {item.facility_id for item in current_facilities}
        new_facilities = set(data or [])

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