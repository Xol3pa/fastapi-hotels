from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityCreate

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_all_facilities(
        db: DBDep
):
    return await db.facilities.get_all()

@router.post("")
async def create_facility(
        db: DBDep,
        data: FacilityCreate,
):
    await db.facilities.add(data)
    await db.commit()

    # test_task.delay()

    return {"success": True}