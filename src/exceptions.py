from datetime import date

from fastapi import HTTPException


class ProjectException(Exception):
    detail = "Something went wrong"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ProjectHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundException(ProjectException):
    detail = "Object not found"


class RoomsAreOccupiedException(ProjectException):
    detail = "Rooms are occupied"


class DuplicateValueException(ProjectException):
    detail = "Duplicate value found"


class InvalidDateRangeHTTPException(ProjectHTTPException):
    status_code = 422
    detail = "Check-in date must be before check-out date"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise InvalidDateRangeHTTPException


class RoomNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Room not found"


class HotelNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Hotel not found"
