from datetime import date

from pydantic import BaseModel
from sqlalchemy import update, delete, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper



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
