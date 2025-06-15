class ProjectException(Exception):
    detail = "Something went wrong"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProjectException):
    detail = "Object not found"


class RoomsAreOccupiedException(ProjectException):
    detail = "Rooms are occupied"


class InvalidDateRangeException(ProjectException):
    detail = "Check-in date must be before check-out date"
