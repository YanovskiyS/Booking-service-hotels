import pytest
from httpx import AsyncClient

from src.utils.db_manager import DBManager
from tests.conftest import get_db_nul_pool


async def test_add_booking(
    authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": 1,
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        },
    )
    assert response.status_code == 200
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "Ok"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_nul_pool():
        await _db.bookings.delete()
        await _db.commit()

@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_rooms",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-03", "2024-08-12", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    delete_all_bookings,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_rooms





