import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start() # Мокаем кеширование

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.main import app
from src.config import settings
from src.database import engine_null_pull, Base, async_session_maker_null_pull
from src.schemas.facilities import RoomFacilityCreate, FacilityCreate
from src.schemas.hotels import HotelCreate
from src.schemas.rooms import RoomCreateWithHotel
from src.utils.db_manager import DBManager
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'


async def get_db_null_pull() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pull():
        yield db


app.dependency_overrides[get_db] = get_db_null_pull


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/hotels_data.json', 'r', encoding='UTF-8') as f:
        hotels_data = json.load(f)
    with open('tests/rooms_data.json', 'r', encoding='UTF-8') as f:
        rooms_data = json.load(f)
    with open('tests/rooms_facilities.json', 'r', encoding='UTF-8') as f:
        rooms_facilities_data = json.load(f)
    with open('tests/facilities.json', 'r', encoding='UTF-8') as f:
        facilities_data = json.load(f)

    validate_hotels = [HotelCreate.model_validate(hotel) for hotel in hotels_data]
    validate_rooms = [RoomCreateWithHotel.model_validate(room) for room in rooms_data]
    validate_rooms_facilities = [RoomFacilityCreate.model_validate(r_f) for r_f in rooms_facilities_data]
    validate_facilities = [FacilityCreate.model_validate(facility) for facility in facilities_data]

    async with DBManager(session_factory=async_session_maker_null_pull) as db_:
        await db_.hotels.add_bulk(validate_hotels)
        await db_.rooms.add_bulk(validate_rooms)
        await db_.facilities.add_bulk(validate_facilities)
        await db_.rooms_facilities.add_bulk(validate_rooms_facilities)
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

@pytest.fixture(scope="session")
async def auth_ac(ac, register_user):
    response = await ac.post(
        '/auth/login',
        json={
            'email': 'test@mail.ru',
            'password': '123412341234',
        }
    )

    assert response.status_code in [200, 201]
    assert 'access_token' in response.cookies

    yield ac
