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


    async def add(self, hotel_data: Hotel):
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump()).returning(HotelsOrm)
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        return await self.session.execute(add_hotel_stmt)
