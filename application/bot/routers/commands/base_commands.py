from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

from appeal_to_service import check_user_in_database

router = Router(name=__name__)


@router.message(CommandStart())
async def start_bot(message: types.Message):
    """Check user login or register"""
    check_user = await check_user_in_database(idd=message.chat.id)
    link = "https://i.ytimg.com/vi/Hd66J_hWlNk/maxresdefault.jpg"
    if "detail" in check_user:
        await message.answer(
            text=f"{markdown.hide_link(link)}Hello {markdown.hbold('My friend')}!",
        )
        await message.answer(
            text="You need to register in this chat, please enter /create"
        )
    else:
        await message.answer(
            text=f"{markdown.hide_link(link)}Hello "
            f"{markdown.hbold(check_user.get('username'))}! "
            f"I will help you develop your desired habit and make your life better!",
        )
        await message.answer(
            text="You will need a token to give you access to manage your habits."
            " If you dont have a token, please enter /token"
        )


@router.message(Command("help"))
async def help_bot(message: types.Message):
    """Command helper"""
    await message.answer(
        text=f"\n/start - {markdown.hbold('start connecting with a bot')} "
        f"\n/help - {markdown.hbold('commands assistant')} "
        f"\n/create - {markdown.hbold('create a user')} "
        f"\n/token - {markdown.hbold('create a token')} "
        f"\n/add_habit - {markdown.hbold('create a habit')} "
        f"\n/get_habits - {markdown.hbold('get list of habits')} "
        f"\n/edit_habit - {markdown.hbold('update or delete any habit')} "
        f"\n/track_habit - {markdown.hbold('mark a habit')} "
        f"\n/habit_stats - {markdown.hbold('look at statistics of habits')} "
        f"\n/set_reminder - {markdown.hbold('set time for reminding of any habit')} "
        f"\n/cancel - {markdown.hbold('resetting current actions')} "
    )
