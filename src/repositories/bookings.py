from datetime import date

from celery.worker.consumer.mingle import exception
from pydantic import BaseModel
from sqlalchemy import update, delete, select, insert

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_price(self, room_id: int):
        query = select(RoomsOrm).filter_by(id=room_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def get_bookings_with_checkin(self):
        query = (
            select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        )

        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]

    async def add_booking(self, data: BaseModel):
        room_ids_for_booking = rooms_ids_for_booking(data.date_from, data.date_to)
        result = await self.session.execute(room_ids_for_booking)
        if data.room_id in result.scalars().all():
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        else:
            raise Exception







