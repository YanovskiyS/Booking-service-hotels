from fastapi import FastAPI, Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])



hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(default=1, description="Номер Сраницы"),
        per_page: int | None = Query(default=2, description="Колличество отелей на странице")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_[(page-1) * per_page: (page-1) * per_page + per_page]

@router.post("")
def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={"1": {"summary": "Сочи", "value": {
                            "title": "Лучший Сочинский отель",
                            "name": "Приезжай не стеснфйся"}},
                      "2": {"summary": "Дубай", "value": {
                            "title": "Дубай, Дубай, Воронеж!",
                            "name": "ДубайВоронеж"
                      }}
                                                            })):

    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                  "title": hotel_data.title,
                  "name": hotel_data.name})
    return  {"status": "Ok"}



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