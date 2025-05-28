from typing import TypeVar, Generic

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper(Generic[DBModelType, SchemaType]):
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, db_entity):
        # Преобразование из DB модели в Pydantic схему
        return cls.schema.model_validate(db_entity, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, domain_entity):
        # Преобразование из Pydantic схемы в DB модель
        return cls.db_model(**domain_entity.model_dump())