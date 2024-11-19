import pytest
from sqlalchemy import select
from models.user_models import User
from tests.factories.factory_boy import session


@pytest.mark.asyncio
async def test_user_status_code_and_existing(db_client, user_factory):
    user = user_factory.create()
    await session.commit()
    response = db_client.get(f"/user/{user.telegram_id}")
    user = await session.execute(select(User))
    assert len(user.scalars().all()) == 1
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_successful_response_content(db_client, user_factory):
    user = user_factory.create()
    await session.commit()
    response = db_client.get(f"/user/{user.telegram_id}")
    assert response.json() == {
        "username": user.username,
        "telegram_id": user.telegram_id,
    }


@pytest.mark.asyncio
async def test_user_response_failed(db_client):
    response = db_client.get(f"/user/100")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_user_successful_response_content_and_data(db_client):
    data = {
        "username": "user",
        "telegram_id": 1,
        "password": "user12345",
    }
    response = db_client.post("/user", json=data)
    user = await session.execute(select(User))
    user = user.scalars().first()
    assert response.json() == {"status": True}
    assert isinstance(user, User)
    assert user.username == "user"
    assert user.telegram_id == 1


@pytest.mark.parametrize("username", [100, True])
@pytest.mark.asyncio
async def test_user_fail_status_code(db_client, username):
    data = {
        "username": username,
        "telegram_id": 1,
        "password": "user12345",
    }
    response = db_client.post("/user", json=data)
    assert response.status_code == 422
