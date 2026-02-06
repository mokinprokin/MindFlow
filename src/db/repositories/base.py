from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from .base_mapper import DataMapper


class BaseRepository:
    model = None
    schema: BaseModel = None
    mapper: DataMapper = DataMapper

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model, self.schema)
            for model in result.scalars().all()
        ]

    async def delete_all(self) -> None:
        query = delete(self.model)
        await self.session.execute(query)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.mapper.map_to_domain_entity(model, self.schema)

    async def create(self, data: BaseModel | dict):
        if isinstance(data, BaseModel):
            insert_data = data.model_dump()
        else:
            insert_data = data

        query = insert(self.model).values(**insert_data).returning(self.model)
        result = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(result.scalar_one(), self.schema)

    async def create_bulk(self, data: list[BaseModel]):
        query = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(query)
        return {"responce": "ok"}
    async def get_filtered(self, **filter_by):
        query = select(self.model)
        
        for key, value in filter_by.items():
            if isinstance(value, list):
                query = query.where(getattr(self.model, key).in_(value))
            else:
                query = query.where(getattr(self.model, key) == value)
                
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model, self.schema)
            for model in result.scalars().all()
        ]
    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(query)
        return self.mapper.map_to_domain_entity(result.scalar_one(), self.schema)

    async def delete(self, **filter_by):
        query = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.rowcount
