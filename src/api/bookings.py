from fastapi import Query, Body, APIRouter
from datetime import date

from src.api.dependencies import UserIdDep
from src.database import async_session_maker


from src.repositories.bookings import BookingsRepository

from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("")
async def create_booking(db: DBDep, user_id: UserIdDep,  booking_data: BookingAddRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    total_price = (booking_data.date_to - booking_data.date_from).days * room.price
    user = user_id
    _booking_data = BookingAdd(user_id=user, price=total_price, **booking_data.model_dump())
    async with async_session_maker() as session:
        booking = await BookingsRepository(session).add(_booking_data)
        await session.commit()

    return {"status": "Ok", "data": booking}


