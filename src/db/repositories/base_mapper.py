from pydantic import BaseModel
from ..database import Base


class DataMapper:
    @classmethod
    def map_to_domain_entity(cls, data, schema):
        return schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, db_model: Base, data: BaseModel):
        return db_model(**data.model_dump())
