from typing import Any, AsyncGenerator

import pytest
import json
from httpx import ASGITransport, AsyncClient
from sqlalchemy import True_

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine, engine_null_pul, async_session_maker, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import Hotel, HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_nul_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db():
    async for db in get_db_nul_pool():
        yield db




app.dependency_overrides[get_db] = get_db_nul_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pul.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open ("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open ("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(item) for item in hotels]
    rooms = [RoomAdd.model_validate(item) for item in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac



@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):

    await ac.post("/auth/register", json={"email": "kot@pes.ru",
                                                         "password": "123456",
                                                         "first_name": "Kot",
                                                         "last_name": "Pes"})