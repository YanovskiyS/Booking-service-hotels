from datetime import date

from src.schemas.bookings import Booking, BookingAdd
from src.schemas.hotels import HotelAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id = user_id,
        date_from = date(year=2024, month=8, day=10),
        date_to = date(year=2024, month=8, day=20),
        room_id= room_id,
        price = 2000)



    await db.bookings.add(booking_data)

    await db.bookings.get_filtered(user_id = user_id)


    await db.bookings.delete(user_id=user_id)

    await db.commit()