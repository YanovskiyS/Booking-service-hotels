from src.schemas.facilities import FacilityAdd


async def test_add_facility(db):
    facility_add_data = FacilityAdd(title="WIFI")

    await db.facilities.add(facility_add_data)
    await db.commit()
