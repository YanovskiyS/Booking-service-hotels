from fastapi import APIRouter

from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(facility_data: FacilityAdd, db: DBDep):
    facility = await FacilityService(db).create_facility(facility_data)

    return {"status": "ok", "data": facility}
