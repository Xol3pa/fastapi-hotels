from pydantic import BaseModel, Field, ConfigDict


class HotelAdd(BaseModel):
    title: str
    location: str

    model_config = ConfigDict(from_attributes=True)

class Hotel(HotelAdd):
    id: int

class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Hotel title"),
    location: str | None = Field(None, description="Hotel location"),
