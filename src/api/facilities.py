from typing import Optional
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    FacilityNameAlreadyExistsException,
    FacilityNameAlreadyExistsHTTPException,
)
from src.schemas.facilities import FacilityCreate, Facility
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(db: DBDep) -> Optional[list[Facility]]:
    """Возвращает все возможные удобства"""

    return await FacilitiesService(db).get_all_facilities()


@router.post("")
async def create_facility(
    db: DBDep,
    data: FacilityCreate,
):
    """Создание удобства"""

    try:
        await FacilitiesService(db).create_facility(data)
    except FacilityNameAlreadyExistsException:
        raise FacilityNameAlreadyExistsHTTPException

    return {"success": True}
