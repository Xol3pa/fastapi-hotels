import logging
import uvicorn
import sys
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi import FastAPI
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api import main_router
from src.init import redis_connector


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    await redis_connector.close()


# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan)

app.include_router(main_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
            reload=True,
            host="0.0.0.0",
            port=8000,
    )
