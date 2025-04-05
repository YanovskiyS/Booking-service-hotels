from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select
from watchfiles import awatch

from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import  PaginationDep
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(paginations: PaginationDep,
        location: str | None = Query(None, description="Расположение"),
        title: str | None = Query(None, description="Название отеля")
        ):
        per_page = paginations.per_page or 5
        async with async_session_maker() as session:
           return await HotelsRepository(session).get_all(location=location,
                                                          title=title,
                                                          limit=per_page,
                                                          offset=per_page * (paginations.page - 1),)




@router.post("")
async def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={"1": {"summary": "Сочи", "value": {
                            "title": "Отель Rich 5 звезд",
                            "location": "г. Сочи, ул. Морская, д. 3"}},
                      "2": {"summary": "Дубай", "value": {
                            "title": "Rich hotel 5 stars",
                            "location": "Dubai, Sheih street 15"
                      }}
                                                            })):

    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        hotel = result.scalar()

        await session.commit()

    return  {"status": "Ok", "data": hotel}



@router.put("/{hotel_id}")
def full_update_hotel(hotel_id: int, hotel_data: Hotel):
    global  hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "Ok"}


@router.patch("/{hotel_id}")
def partial_update_hotel(hotel_id: int, hotel_data: HotelPatch):
    global  hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return  {"status": "Ok"}



@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global  hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}