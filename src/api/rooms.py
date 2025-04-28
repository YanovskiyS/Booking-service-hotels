

from fastapi import Body, APIRouter
from datetime import date


from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep,
                    date_from: date,
                    date_to: date):

    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_rooms(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id)/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    db.commit()

    return  {"status": "Ok", "data": room}

@router.put("/{hotel_id}/rooms/{room_id}")
async def full_update_hotel(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)

    await db.commit()


    return {"status": "Ok"}


@router.patch("/{hotel_id}/{room_id}")
async def partial_update_hotel(db: DBDep, hotel_id: int, room_id: int, rooms_data: RoomPatchRequest):
    _room_data_dict = rooms_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **rooms_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])

    await db.commit()
    return  {"status": "Ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "Ok"}