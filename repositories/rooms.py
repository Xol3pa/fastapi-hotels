from repositories.base import BaseRepository
from src.models.rooms import RoomsModel


class HotelRepository(BaseRepository):
    model = RoomsModel