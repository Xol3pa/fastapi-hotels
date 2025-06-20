from datetime import date
from src.exceptions import InvalidDateRangeException
from .base import BaseValidator


class DateValidator(BaseValidator):

    @staticmethod
    def validate_date_to_after_date_from(date_from: date, date_to: date) -> None:
        """Проверка что дата заезда будет меньше чем дата выезда"""

        if date_from >= date_to:
            raise InvalidDateRangeException