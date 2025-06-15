from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Базовый класс для всех схем с общей конфигурацией"""

    model_config = ConfigDict(from_attributes=True)


class BaseCreateSchema(BaseSchema):
    """Базовый класс для схем создания"""

    pass


class BaseUpdateSchema(BaseSchema):
    """Базовый класс для схем обновления"""

    pass


class BaseResponseSchema(BaseSchema):
    """Базовый класс для схем ответа с ID"""

    id: int
