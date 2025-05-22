from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import Room
from sqlalchemy import select


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_all(
            self,
            hotel_id: int
    ) -> list[Room]:
        query = select(RoomsModel).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

