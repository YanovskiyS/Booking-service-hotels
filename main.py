from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1},
                  )



@app.put("/hotels/{hotel_id}")
def full_update_hotel(title: str, name: str, hotel_id: int):
    global  hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "Ok"}

@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(hotel_id: int,
                         title: str | None = Query(default=None, description="Название"),
                         name: str | None = Query(default=None, description="Имя"),
                         ):
    global  hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
    return  {"status": "Ok"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global  hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "Ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
