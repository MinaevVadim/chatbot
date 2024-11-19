import asyncio
import os
import sys
from datetime import datetime

from pytest_factoryboy import register
import pytest
from starlette.testclient import TestClient

sys.path.append(os.getcwd())

from models import Base
from dependencies import db
from main import app
from tests.factories.factory_boy import (
    UserFactory,
    engine,
    session,
    HabitTrackingFactory,
    HabitFactory,
)

register(UserFactory)
register(HabitTrackingFactory)
register(HabitFactory)


async def create_and_drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def override():
        async with session() as session_for_override:
            async with session_for_override.begin():
                yield session_for_override

    app.dependency_overrides[db] = override


@pytest.fixture(scope="session", autouse=True)
def db_create():
    asyncio.run(create_and_drop_tables())
    yield


async def clean_tables():
    for tbl in reversed(Base.metadata.sorted_tables):
        await session.execute(tbl.delete())
        await session.commit()


@pytest.fixture
def db_client():
    client = TestClient(app)
    yield client
    asyncio.run(clean_tables())


@pytest.fixture
async def create_habit(user_factory, habit_factory, habit_tracking_factory):
    user = user_factory.create()
    await session.commit()
    habit = habit_factory.create(user=user.id)
    await session.commit()
    habit_track = habit_tracking_factory.create(habit=habit.id)
    await session.commit()
    return user, habit, habit_track
