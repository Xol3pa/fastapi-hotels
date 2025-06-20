from typing import Optional

from src.exceptions import DuplicateValueException, FacilityNameAlreadyExistsException
from src.schemas.facilities import FacilityCreate, Facility
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    """Сервисный слой для эндпоинтов /facilities"""

    async def get_all_facilities(self) -> Optional[list[Facility]]:
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityCreate):
        try:
            await self.db.facilities.add(data)
        except DuplicateValueException:
            raise FacilityNameAlreadyExistsException
        await self.db.commit()

        test_task.delay()