from datetime import date

from fastapi import Query, Body, APIRouter
from fastapi_cache.decorator import cache


from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(paginations: PaginationDep,
                     db: DBDep,
                     date_from: date,
                     date_to: date,
                     location: str | None = Query(None, description="Расположение"),
                     title: str | None = Query(None, description="Название отеля"),

                     ):
        per_page = paginations.per_page or 5

        return await db.hotels.get_filtered_by_time(date_from=date_from, date_to=date_to, location=location, title=title,
                                                    limit=per_page, offset=per_page * (paginations.page - 1),)



@router.get("/{hotels_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_by_id(hotel_id)



@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(
    openapi_examples={"1": {"summary": "Сочи", "value": {
                            "title": "Отель Rich 5 звезд",
                            "location": "г. Сочи, ул. Морская, д. 3"}},
                      "2": {"summary": "Дубай", "value": {
                            "title": "Rich hotel 5 stars",
                            "location": "Dubai, Sheih street 15"
                      }}
                                                            })):

    hotel = await db.hotels.add(hotel_data)
    return  {"status": "Ok", "data": hotel}



@router.put("/{hotel_id}")
async def full_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):

    await db.hotels.edit(hotel_data, id=hotel_id)
    return {"status": "Ok"}


@router.patch("/{hotel_id}")
async def partial_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    return  {"status": "Ok"}



@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    return {"status": "Ok"}