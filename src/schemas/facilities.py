from pydantic import Field

from . import BaseCreateSchema, BaseResponseSchema


class FacilityCreate(BaseCreateSchema):
    """Схема для создания удобства"""

    title: str = Field(..., description="Название удобства")


class Facility(BaseResponseSchema):
    """Схема удобства для ответа"""

    title: str = Field(..., description="Название удобства")


class RoomFacilityCreate(BaseCreateSchema):
    """Схема для привязки удобства к комнате"""

    room_id: int = Field(..., description="ID комнаты")
    facility_id: int = Field(..., description="ID удобства")


class RoomFacility(BaseResponseSchema):
    """Схема связи комната-удобство для ответа"""

    room_id: int = Field(..., description="ID комнаты")
    facility_id: int = Field(..., description="ID удобства")
