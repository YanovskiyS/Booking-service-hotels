from pydantic import BaseModel
from sqlalchemy import update, delete, select

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_price(self, room_id: int):
        query = select(RoomsOrm).filter_by(id=room_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
