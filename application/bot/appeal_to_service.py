import aiohttp


async def check_user_in_database(idd: int) -> dict:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        response = await client.get(f"http://127.0.0.1:8000/user/{idd}")
        user = await response.json()
        return user


async def create_new_user(dct: dict) -> None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        await client.post("http://127.0.0.1:8000/user", json=dct)


async def get_token_for_user(dct: dict) -> dict | None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        response = await client.post("http://127.0.0.1:8000/token", json=dct)
        result = await response.json()
        return result


async def add_habit_for_user(dct: dict) -> None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        await client.post("http://127.0.0.1:8000/habit", json=dct)


async def check_token_for_user(token: str) -> bool:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        response = await client.get(f"http://127.0.0.1:8000/token/{token}")
        result = await response.json()
        return result


async def get_habits_for_user(idd: int) -> list:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        response = await client.get(f"http://127.0.0.1:8000/habit/user/{idd}")
        result = await response.json()
        return result


async def get_habit_for_user(idd: int) -> dict:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        response = await client.get(f"http://127.0.0.1:8000/habit/{idd}")
        result = await response.json()
        return result


async def update_habits_for_user(idd: int, data: dict) -> None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        await client.patch(f"http://127.0.0.1:8000/habit/{idd}", json=data)


async def delete_habit_for_user(idd: int) -> None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        await client.delete(f"http://127.0.0.1:8000/habit/{idd}")


async def mark_habit_for_user(idd: int, extra=False) -> None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10)) as client:
        await client.post(f"http://127.0.0.1:8000/habit/{idd}?extra={extra}")
