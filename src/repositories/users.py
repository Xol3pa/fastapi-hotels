from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models.users import UsersModel
from src.repositories.mappers.mappers import UserDataMapper, UserWithPasswordDataMapper
from src.schemas.users import UserWithPassword, User, UserCreateDB


class UsersRepository(BaseRepository):
    model = UsersModel
    mapper = UserDataMapper

    async def get_all(self, *args, **kwargs) -> list[User]:
        return await super().get_all(*args, **kwargs)

    async def get_one_or_none(self, **filter_by) -> Optional[User]:
        return await super().get_one_or_none(**filter_by)

    async def get_filtered(self, *filter, **filter_by) -> list[User]:
        return await super().get_filtered(*filter_by, **filter_by)

    async def add(self, data: UserCreateDB) -> Optional[User]:
        return await super().add(data)

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithPassword:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return UserWithPasswordDataMapper.map_to_domain_entity(model)
