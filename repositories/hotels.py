from repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from sqlalchemy import select, func, insert, literal_column


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
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

        return result.scalars().all()

    async def add(
            self,
            **hotel_data,
    ):
        add_hotel_stmt = (
            insert(self.model)
            .values(**hotel_data)
            .returning(self.model)
        )
        result = await self.session.execute(add_hotel_stmt)

        return result.scalars().all()