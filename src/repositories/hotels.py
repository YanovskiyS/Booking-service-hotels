from pydantic import BaseModel
from sqlalchemy import select, func, insert, literal_column

from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel



class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()


    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by):
        product_update = select(self.model).filter_by(**filter_by)
        updated = await self.session.scalar(product_update)
        updated.title = data.title
        updated.location = data.location
        await self.session.execute(product_update)

    async def delete(self, **filter_by):
        product_delete = select(self.model).filter_by(**filter_by)
        deleted = await self.session.scalar(product_delete)
        await self.session.delete(deleted)


