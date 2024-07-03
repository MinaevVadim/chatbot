import asyncio
import logging

from aiogram import Dispatcher

from config_schedule import schedule
from routers import router as main_router
from my_bot import bot

dp = Dispatcher()

dp.include_router(main_router)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    schedule.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
