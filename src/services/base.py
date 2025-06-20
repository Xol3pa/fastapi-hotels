from src.services.validators import EntityValidator, DateValidator
from src.utils.db_manager import DBManager
from src.utils.meta.docstring import DocstringRequiredMeta


class BaseService(metaclass=DocstringRequiredMeta):
    """Базовая реализация сервисного слоя"""

    db: DBManager | None

    def __init__(self, db: DBManager | None = None) -> None:
        self.db = db
        self.entity_validator = EntityValidator(db)
        self.date_validator = DateValidator(db)
