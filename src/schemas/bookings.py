from datetime import date
from pydantic import BaseModel


class BookingAdd(BaseModel):
    user_id: int
    date_from: date
    date_to: date
    room_id: int
    price: int


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class Booking(BookingAdd):
    id: int
