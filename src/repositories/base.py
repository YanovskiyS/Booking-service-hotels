from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.dialects.mysql import insert

from src.exceptions import ObjectNotFoundException, HotelIsNotExist
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filtered_by):
        query = select(self.model).filter(*filter).filter_by(**filtered_by)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None

        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(add_data_stmt)
        except IntegrityError:
            raise HotelIsNotExist
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        product_update = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(product_update)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
