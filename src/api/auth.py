from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserEmailAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
    IncorrectPasswordHTTPException,
    IncorrectPasswordException,
    UserEmailAlreadyExistsException,
)
from src.schemas.users import UserCreate, User
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентицифкация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserCreate,
):
    """Регистрация"""

    try:
        await AuthService(db).register_user(data)
    except UserEmailAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"success": True}


@router.post("/login")
async def login_user(db: DBDep, data: UserCreate, response: Response):
    """Аутентификация"""

    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {
        "access_token": access_token,
    }


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Выход из аккаунта"""

    response.delete_cookie("access_token")
    return {"success": True}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep) -> User:
    """Получение данных профиля"""

    try:
        user = await AuthService(db).get_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return user
