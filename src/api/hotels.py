from datetime import date
from fastapi import HTTPException

from fastapi import Query, Body, APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import HotelIsNotExist
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    paginations: PaginationDep,
    db: DBDep,
    date_from: date,
    date_to: date,
    location: str | None = Query(None, description="Расположение"),
    title: str | None = Query(None, description="Название отеля"),
):
    return await HotelService(db).get_filtered_by_time(
        paginations, date_from, date_to, location, title
    )


@router.get("/{hotels_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except HotelIsNotExist as err:
        raise HTTPException(status_code=404, detail=err.detail)


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Rich 5 звезд",
                    "location": "г. Сочи, ул. Морская, д. 3",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Rich hotel 5 stars",
                    "location": "Dubai, Sheih street 15",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "Ok", "data": hotel}


@router.put("/{hotel_id}")
async def full_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).full_update_hotel(hotel_data, id=hotel_id)
    return {"status": "Ok"}


@router.patch("/{hotel_id}")
async def partial_update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).partial_update_hotel(
        hotel_data, hotel_id, exclude_unset=True
    )

    return {"status": "Ok"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "Ok"}
