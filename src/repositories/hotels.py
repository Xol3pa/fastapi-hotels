from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from sqlalchemy import select, func

from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ) -> list[Hotel]:
        query = select(HotelsModel)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(func.lower(location)))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(func.lower(title)))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
