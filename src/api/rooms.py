from fastapi import APIRouter
from datetime import date


from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep, date_from: date, date_to: date):
    try:
        return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one(hotel_id=hotel_id, id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id)/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "Ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def full_update_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest
):
    await RoomService(db).full_update_room(hotel_id, room_id, room_data)

    return {"status": "Ok"}


@router.patch("/{hotel_id}/{room_id}")
async def partial_update_hotel(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    await RoomService(db).partial_update_room(hotel_id, room_id, room_data)
    return {"status": "Ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "Ok"}
