import asyncio
import json
from datetime import datetime

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient
from httpx import AsyncClient
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.config import settings
from src.database import engine, Base, async_session_maker
from src.hotels.models import *
from src.main import app as fastapi_app
from src.users.auth import get_password_hash
from src.users.models import User
from src.bookings.models import Booking


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def setup_db(session: AsyncSession):
    print(settings.MODE)
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    names = {"hotels": Hotel, "rooms": Room, "users": User, "bookings": Booking}
    for json_name, table_name in names.items():
        with open(f"tests/test_data/{json_name}.json", encoding="utf-8") as file:
            values = json.load(file)

        if json_name == "bookings":
            for val in values:
                val["date_from"] = datetime.strptime(val["date_from"], "%Y-%m-%d")
                val["date_to"] = datetime.strptime(val["date_to"], "%Y-%m-%d")
        if json_name == "users":
            for user in values:
                user["hashed_password"] = get_password_hash(user["hashed_password"])
        await session.execute(insert(table_name), values)
        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def startup_redis():
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            url="/v1/users/login",
            json={
                "email": "fedor@moloko.ru",
                "password": "fedor"
            }
        )
        assert ac.cookies["booking_access_token"]
        yield ac
