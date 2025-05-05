from src.api.dependencies import UserIdDep
from src.exceptions import RoomNotFoundException, ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService


class BookingService(BaseService):
    async def create_booking(self,
            user_id: UserIdDep, booking_data: BookingAddRequest
    ):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        hotel = await self.db.hotels.get_one_or_none(id=room.hotel_id)
        total_price = (booking_data.date_to - booking_data.date_from).days * room.price
        _booking_data = BookingAdd(
            user_id=user_id, price=total_price, **booking_data.model_dump()
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)