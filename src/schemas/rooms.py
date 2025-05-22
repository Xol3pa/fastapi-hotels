from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict


HotelId = Annotated[int, Field(..., description="Hotel ID")]
RoomId = Annotated[int, Field(..., description="Room ID")]
Title = Annotated[str, Field(description="Room title")]
Price = Annotated[int, Field(description="Room price")]
Quantity = Annotated[int, Field(description="Room quantity")]
Description = Annotated[str, Field(description="Room description")]


class RoomBase(BaseModel):
    title: Title = Field(...)
    price: Price = Field(...)
    quantity: Quantity = Field(...)
    description: Description = Field(...)

    model_config = ConfigDict(from_attributes=True)

class RoomAdd(RoomBase):
    pass

class RoomAddWithHotelId(RoomAdd):
    hotel_id: HotelId

class RoomPatch(RoomBase):
    title: Optional[Title] = None
    price: Optional[Price] = None
    quantity: Optional[Quantity] = None
    description: Optional[Description] = None

class Room(RoomAddWithHotelId):
    id: RoomId