from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_one_or_raise(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        objs = result.scalars().all()

        if len(objs) == 0:
            raise HTTPException(status_code=404, detail="Object not found")
        if len(objs) > 1:
            raise HTTPException(status_code=400, detail="Multiple objects found")

        return objs[0]

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        await self.get_one_or_raise(**filter_by)

        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        await self.session.execute(edit_data_stmt)

    async def delete(self, **filter_by) -> None:
        await self.get_one_or_raise(**filter_by)

        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)