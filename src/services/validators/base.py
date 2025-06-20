from abc import ABC
from src.utils.db_manager import DBManager


class BaseValidator(ABC):
    db: DBManager | None

    def __init__(self, db: DBManager):
        self.db = db
