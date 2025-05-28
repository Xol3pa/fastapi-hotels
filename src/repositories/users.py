from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersModel
from src.repositories.mappers.mappers import UserDataMapper, UserWithPasswordDataMapper
from src.schemas.users import UserWithPassword


class UsersRepository(BaseRepository):
    model = UsersModel
    mapper = UserDataMapper

    async def get_user_with_hashed_password(
            self,
            email: EmailStr
    ) -> UserWithPassword | None:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None

        return UserWithPasswordDataMapper.map_to_domain_entity(model)

