from datetime import date

from fastapi import Query, Body, APIRouter


from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.schemas.facilities import FacilityAdd
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(facility_data: FacilityAdd, db: DBDep, ):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "ok", "data": facility}
