from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(settings.db_url)
engine_null_pull = create_async_engine(settings.db_url, poolclass=NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pull = async_sessionmaker(bind=engine_null_pull, expire_on_commit=False)

class Base(DeclarativeBase):
    pass