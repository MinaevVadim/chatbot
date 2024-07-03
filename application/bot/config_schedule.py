import emoji
from aiogram import Bot
from aiogram.utils import markdown
from apscheduler.schedulers.asyncio import AsyncIOScheduler


schedule = AsyncIOScheduler(timezone="Europe/Moscow")


async def send_some_message(name_habit: str, chat_idd: int, bot_sender: Bot):
    """Displaying information about the notification"""
    text = (
        f"Do not forget to mark your habit "
        f"{markdown.hbold(name_habit)} today!"
        f" {emoji.emojize(':alarm_clock:')}"
        f" {emoji.emojize(':right_arrow:')} /track_habit"
    )
    await bot_sender.send_message(chat_id=chat_idd, text=text)


async def schedule_attack(
    name_habit: str,
    bot_father: Bot,
    chat_idd: int,
    hour: int = 18,
    minute: int = 30,
):
    """Configuration of notification of habits"""
    schedule.add_job(
        send_some_message,
        trigger="cron",
        hour=hour,
        minute=minute,
        kwargs={
            "name_habit": name_habit,
            "chat_idd": chat_idd,
            "bot_sender": bot_father,
        },
    )
