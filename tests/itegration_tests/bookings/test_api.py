import pytest
from sqlalchemy import Table, text
from sqlalchemy.testing.suite.test_reflection import metadata

from src.database import engine_null_pul, Base, async_session_maker_null_pool
from src.models.bookings import BookingsOrm
from src.utils.db_manager import DBManager


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",
                         [(1, "2024-08-01", "2024-08-10", 200),
                          (1, "2024-08-01", "2024-08-10", 200),
                          (1, "2024-08-01", "2024-08-10", 200),
                          (1, "2024-08-01", "2024-08-10", 200),
                          (1, "2024-08-01", "2024-08-10", 200),
                          (1, "2024-08-01", "2024-08-10", 500)])

async def test_add_booking(room_id, date_from, date_to, status_code,
        db, authenticate_ac):
    response = await authenticate_ac.post("/bookings", json={"room_id": room_id,
                                                  "date_from": date_from,
                                                  "date_to": date_to
                                                  })
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "Ok"
        assert isinstance(res, dict)
        assert "data" in res


@pytest.fixture(scope="session", autouse=False)
async def clean_specific_table():
    async with engine_null_pul.begin() as conn:
        table_name = "bookings"
        table = Base.metadata.tables[table_name]
        await conn.execute(table.delete())


@pytest.mark.parametrize("room_id, date_from, date_to, quantity",
                         [(1, "2024-08-01", "2024-08-10", 1),
                          (1, "2024-08-01", "2024-08-10", 2),
                          (1, "2024-08-01", "2024-08-10", 3)])
async def test_add_and_get_my_bookings(room_id, date_from, date_to, quantity, clean_specific_table, authenticate_ac):
    await authenticate_ac.post("/bookings", json={"room_id": room_id,
                                                             "date_from": date_from,
                                                             "date_to": date_to
                                                             })
    get_response = await authenticate_ac.get("/bookings/me")
    res = get_response.json()
    assert len(res) == quantity






