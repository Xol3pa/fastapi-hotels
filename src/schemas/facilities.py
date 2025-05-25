from pydantic import BaseModel, ConfigDict, Field


class BaseFacilities(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class FacilityDataRequest(BaseFacilities):
    title: str = Field(..., description="Facility title")

class Facility(FacilityDataRequest):
    id: int
