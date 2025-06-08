import json

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert

from src.main import app
from src.config import settings
from src.database import engine_null_pull, Base
from src.models import *
from src.schemas.hotels import HotelCreate


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='session', autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        with open('tests/hotels_data.json', 'r', encoding='UTF-8') as f:
            hotels_data = json.load(f)
            hotel_stmt = insert(HotelsModel).values(hotels_data)

            await conn.execute(hotel_stmt)

        with open('tests/rooms_data.json', 'r', encoding='UTF-8') as f:
            rooms_data = json.load(f)
            rooms_stmt = insert(RoomsModel).values(rooms_data)

            await conn.execute(rooms_stmt)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as api:
        response = await api.post(
            '/auth/register',
            json={
                'email': 'test@mail.ru',
                'password': '123412341234',
            })

        assert(response.status_code in [200, 201])