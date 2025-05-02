from fastapi import APIRouter, HTTPException
from datetime import date


from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.exceptions import ObjectNotFoundException, HotelIsNotExist
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep, date_from: date, date_to: date):
    if date_to < date_from:
        raise HTTPException(status_code=409, detail="Дата выезда позже даты заезда")
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данного номера не существует")


@router.post("/{hotel_id)/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except HotelIsNotExist as err:
        raise HTTPException(status_code=409, detail=err.detail)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    db.commit()

    return {"status": "Ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def full_update_hotel(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest
):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данной комнаты не существует")
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id, facilities_ids=room_data.facilities_ids
    )

    await db.commit()

    return {"status": "Ok"}


@router.patch("/{hotel_id}/{room_id}")
async def partial_update_hotel(
    db: DBDep, hotel_id: int, room_id: int, rooms_data: RoomPatchRequest
):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данной комнаты не существует")
    _room_data_dict = rooms_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(
        hotel_id=hotel_id, **rooms_data.model_dump(exclude_unset=True)
    )
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.commit()
    return {"status": "Ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Данной комнаты не существует")
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Ok"}
