from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import (
    DuplicateValueException,
    UserNotFoundException,
    IncorrectPasswordException,
    ObjectNotFoundException,
    UserEmailAlreadyExistsException,
    InvalidTokenException,
)
from src.schemas.users import UserCreate, UserCreateDB
from src.services.base import BaseService


class AuthService(BaseService):
    """Сервисный слой для эндпоинтов /auth"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.InvalidTokenError:
            raise InvalidTokenException

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    async def register_user(self, data: UserCreate):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserCreateDB(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(data=new_user_data)
            await self.db.commit()
        except DuplicateValueException:
            raise UserEmailAlreadyExistsException

    async def login_user(self, data: UserCreate):
        try:
            user = await self.db.users.get_user_with_hashed_password(email=data.email)
        except ObjectNotFoundException:
            raise UserNotFoundException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException

        access_token = AuthService().create_access_token(data={"user_id": user.id})

        return access_token

    async def get_user(self, user_id: int):
        return await self.entity_validator.validate_user_exists(id=user_id)
