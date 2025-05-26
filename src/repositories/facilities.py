from src.models.facilities import Facilities, RoomsFacilities
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacility