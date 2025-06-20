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


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class UserNotFoundException(ObjectNotFoundException):
    detail = "User not found"


class FacilityNotFoundException(ObjectNotFoundException):
    detail = "Facility not found"


class BookingsNotFoundException(ObjectNotFoundException):
    detail = "Bookings not found"


class RoomsAreOccupiedException(ProjectException):
    detail = "Rooms are occupied"


class DuplicateValueException(ProjectException):
    detail = "Duplicate value found"


class UserEmailAlreadyExistsException(ProjectException):
    detail = "User email already exists"


class FacilityNameAlreadyExistsException(DuplicateValueException):
    detail = "Facility name already exists"


class InvalidDeleteOptionsException(ProjectException):
    detail = "Delete operation requires filters or explicit force_delete_all=True"


class IncorrectPasswordException(ProjectException):
    detail = "Incorrect password"


class InvalidTokenException(ProjectException):
    detail = "Invalid token"


class InvalidDateRangeException(ProjectException):
    detail = "Invalid date range"


# HTTPExceptions

class InvalidDateRangeHTTPException(ProjectHTTPException):
    status_code = 422
    detail = "Check-in date must be before check-out date"


class InvalidAccessTokenHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Invalid access token"

class RoomNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Room not found"


class HotelNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Hotel not found"


class FacilityNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Facility not found"

class InvalidDeleteOptionsHTTPException(ProjectHTTPException):
    status_code = 400
    detail = "Delete operation requires filters or explicit force_delete_all=True"


class UserEmailAlreadyExistsHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "User email already exists"


class FacilityNameAlreadyExistsHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "Facility name already exists"


class UserNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "User not found"


class IncorrectPasswordHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Incorrect password"


class RoomsAreOccupiedHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Rooms are occupied"