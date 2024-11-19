import pytest

from tests.factories.factory_boy import session


@pytest.mark.asyncio
async def test_token_status_code_and_content(db_client, user_factory):
    user = user_factory.create()
    await session.commit()
    data = {
        "username": user.username,
        "telegram_id": user.telegram_id,
        "password": "qwery",
    }
    response = db_client.post("/token", json=data)
    token = response.json()["access_token"]
    assert response.status_code == 201
    assert response.json() == {"access_token": token, "type": "bearer"}


@pytest.mark.asyncio
async def test_token_status_code_fail(db_client):
    data = {
        "username": "fake_user",
        "telegram_id": "fake_id",
        "password": "fake_password",
    }
    response = db_client.post("/token", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize("token", [True, 100, "8888", "!)9!"])
@pytest.mark.asyncio
async def test_get_token_fail(db_client, token):
    response = db_client.get(f"/token/{token}")
    assert response.json() == {"detail": "Token is not valid."}
    assert response.status_code == 401
