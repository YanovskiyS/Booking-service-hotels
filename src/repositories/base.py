from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import selectinload


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filtered_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filtered_by)
                 )
        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


    async def get_all(self, *args, **kwargs):
        return  await self.get_filtered()




    async def get_one_or_none(self, **filter_by):
        '''query = select(self.model).filter_by(**filter_by)'''
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        product_update = (update(self.model).filter_by(**filter_by)
                          .values(data.model_dump(exclude_unset=exclude_unset))).returning(self.model)
        result = await self.session.execute(product_update)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)


    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
