from pydantic import BaseModel
from sqlalchemy import update, delete

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        product_update = (update(self.model).filter_by(**filter_by)
                          .values(data.model_dump(exclude_unset=exclude_unset)))
        await self.session.execute(product_update)

    '''async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)'''