from src.database import async_session_maker_null_pull
from src.schemas.hotels import HotelCreate
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelCreate(title="Test Hotel", location="New York")

    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel_data}")