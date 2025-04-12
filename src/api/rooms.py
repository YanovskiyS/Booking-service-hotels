from fastapi import Body, APIRouter

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.post("/hotels")
async def create_room(room_data: RoomAdd):

    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return  {"status": "Ok", "data": room}

@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(id=hotel_id)

@router.put("/{hotel_id}/{room_id}")
async def full_update_hotel(hotel_id: int, room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:

        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "Ok"}


@router.patch("/{hotel_id}/{room_id}")
async def partial_update_hotel(hotel_id: int, room_id: int, rooms_data: RoomPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(rooms_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return  {"status": "Ok"}


@router.delete("/{hotel_id}/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "Ok"}