from datetime import date
from fastapi import HTTPException

from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        paginations,
        date_from: date,
        date_to: date,
        location: str | None,
        title: str | None,
    ):
        if date_to < date_from:
            raise HTTPException(status_code=409, detail="Дата выезда позже даты заезда")
        per_page = paginations.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (paginations.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_by_id(hotel_id)

    async def create_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def full_update_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, hotel_id)

    async def partial_update_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        await self.db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
