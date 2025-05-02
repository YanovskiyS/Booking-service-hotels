

from fastapi import APIRouter, HTTPException

from src.api.dependencies import UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
    db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest
):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    total_price = (booking_data.date_to - booking_data.date_from).days * room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=total_price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as err:
        raise HTTPException(status_code=409, detail=err.detail)
    await db.commit()

    return {"status": "Ok", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
