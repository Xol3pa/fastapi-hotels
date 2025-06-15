from typing import Optional, List, Any

from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs) -> List[Any]:
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_filtered(self, *filter, **filter_by) -> List[Any]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_or_none(self, **filter_by) -> Optional[Any]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None

        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> Optional[Any]:
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()

        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]) -> None:
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])

        await self.session.execute(add_data_stmt)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        await self.session.execute(edit_data_stmt)

    async def delete(
        self, *filter, force_delete_all: bool = False, **filter_by
    ) -> None:
        if not filter and not filter_by and not force_delete_all:
            raise ValueError(
                "Delete operation requires filters or explicit force_delete_all=True"
            )

        delete_stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
