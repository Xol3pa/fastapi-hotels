from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import DuplicateValueException
from src.schemas.users import UserCreate, UserCreateDB
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентицифкация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserCreate,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserCreateDB(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(data=new_user_data)
        await db.commit()
    except DuplicateValueException:
        raise HTTPException(status_code=409, detail="This email already registered")

    return {"success": True}


@router.post("/login")
async def login_user(db: DBDep, data: UserCreate, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = AuthService().create_access_token(data={"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {
        "access_token": access_token,
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"success": True}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user
