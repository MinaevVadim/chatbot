import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.habit_models import Habit
from tests.factories.factory_boy import session


@pytest.mark.asyncio
async def test_create_habit_status_code_and_existing(db_client, user_factory):
    user = user_factory.create()
    await session.commit()
    data = {
        "telegram_id": user.telegram_id,
        "name_habit": "habit",
        "description": "good habit",
        "habit_goal": "goal habit",
        "count": 0,
    }
    response = db_client.post("/habit/", json=data)
    habit = await session.execute(select(Habit))
    assert len(habit.scalars().all()) == 1
    assert response.status_code == 201
    assert response.json() == {"status": True}


@pytest.mark.asyncio
async def test_create_habit_with_fake_user(db_client):
    data = {
        "telegram_id": 10,
        "name_habit": "habit",
        "description": "bad habit",
        "habit_goal": "goal habit",
        "count": 0,
    }
    response = db_client.post("/habit/", json=data)
    assert response.json() == {"detail": "User does not exist."}
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_habits_with_valid_user(db_client, create_habit):
    user, habit, _ = await create_habit
    response = db_client.get(f"/habit/user/{user.telegram_id}")
    habit = await session.execute(
        select(Habit).options(joinedload(Habit.habit_tracking))
    )
    habit = habit.scalars().first()
    assert response.json() == [
        {
            "id": habit.id,
            "telegram_id": user.telegram_id,
            "name_habit": habit.name_habit,
            "description": habit.description,
            "habit_goal": habit.habit_goal,
            "count": habit.habit_tracking.count,
            "alert_time": None,
        },
    ]
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_habits_with_invalid_user(db_client):
    response = db_client.get("/habit/user/10")
    assert response.json() == {"detail": "User does not exist."}
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_habit_successful(db_client, create_habit):
    user, habit, _ = await create_habit
    response = db_client.get(f"/habit/{habit.id}")
    habit = await session.execute(
        select(Habit).options(joinedload(Habit.habit_tracking))
    )
    habit = habit.scalars().first()
    assert response.json() == {
        "id": habit.id,
        "telegram_id": None,
        "name_habit": habit.name_habit,
        "description": habit.description,
        "habit_goal": habit.habit_goal,
        "count": habit.habit_tracking.count,
        "alert_time": habit.habit_tracking.alert_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_habit_failed(db_client):
    response = db_client.get("/habit/10")
    assert response.json() == {"detail": "Habit does not exist."}
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_habit_successful(db_client, create_habit):
    user, habit, _ = await create_habit
    data = {
        "name_habit": "a new habit",
        "description": "description",
        "habit_goal": "habit goal",
    }
    response = db_client.patch(f"/habit/{habit.id}", json=data)
    habit = await session.execute(select(Habit))
    habit = habit.scalars().first()
    assert response.json() == {"status": True}
    assert response.status_code == 200
    assert habit.name_habit == data["name_habit"]
    assert habit.description == data["description"]
    assert habit.habit_goal == data["habit_goal"]


@pytest.mark.asyncio
async def test_update_habit_failed(db_client):
    data = {
        "name_habit": "some habit",
        "description": "some description",
        "habit_goal": "some habit goal",
    }
    response = db_client.patch("/habit/10", json=data)
    assert response.json() == {"detail": "Habit does not exist."}
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_habit_successful(db_client, create_habit):
    user, habit, _ = await create_habit
    response = db_client.delete(f"/habit/{habit.id}")
    habit = await session.execute(select(Habit))
    habit = habit.scalars().all()
    assert response.json() == {"status": True}
    assert response.status_code == 200
    assert not len(habit)


@pytest.mark.asyncio
async def test_delete_habit_failed(db_client):
    response = db_client.delete("/habit/10")
    assert response.json() == {"detail": "Habit does not exist."}
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_track_habit_successful(db_client, create_habit):
    user, habit, habit_track = await create_habit
    old_count = habit_track.count
    response = db_client.post(f"/habit/{habit.id}")
    habit = await session.execute(
        select(Habit).options(joinedload(Habit.habit_tracking))
    )
    habit = habit.scalars().first()
    assert response.json() == {"status": True}
    assert response.status_code == 200
    assert habit.habit_tracking.count == old_count


@pytest.mark.asyncio
async def test_track_habit_failed(db_client):
    response = db_client.post("/habit/10")
    assert response.json() == {"detail": "Habit does not exist."}
    assert response.status_code == 400
