import json
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.config import settings
from src.database import engine_null_pull, Base, async_session_maker_null_pull
from src.schemas.hotels import HotelCreate
from src.schemas.rooms import RoomCreateWithHotel
from src.utils.db_manager import DBManager
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/hotels_data.json', 'r', encoding='UTF-8') as f:
        hotels_data = json.load(f)
    with open('tests/rooms_data.json', 'r', encoding='UTF-8') as f:
        rooms_data = json.load(f)

    validate_hotels = [HotelCreate.model_validate(hotel) for hotel in hotels_data]
    validate_rooms = [RoomCreateWithHotel.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pull) as db_:
        await db_.hotels.add_bulk(validate_hotels)
        await db_.rooms.add_bulk(validate_rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    response = await ac.post(
        '/auth/register',
        json={
            'email': 'test@mail.ru',
            'password': '123412341234',
        })

    assert(response.status_code in [200, 201])