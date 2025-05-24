from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BookingDataRequest(BookingBase):
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingDataRequest):
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int