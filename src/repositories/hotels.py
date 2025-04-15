from pydantic import BaseModel
from sqlalchemy import select, delete, update


from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel



class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(self, location, title, limit, offset, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(HotelsOrm.title.ilike(f"%{title}%"))
        hotels_ids_to_get = (hotels_ids_to_get
                             .limit(limit)
                             .offset(offset))


        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))

    async def get_by_id(self, hotel_id: int):
        query = select(self.model).filter_by(id=hotel_id)
        result = await self.session.execute(query)
        model =  result.scalars().one_or_none()
        if model is None:
            return  None
        return Hotel.model_validate(model, from_attributes=True)


    '''async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        #print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        Hotel.model_validate(model, from_attributes=True)'''

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        product_update = (update(self.model).filter_by(**filter_by)
                          .values(data.model_dump(exclude_unset=exclude_unset)))
        await self.session.execute(product_update)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)


