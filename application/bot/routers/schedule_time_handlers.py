from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_schedule import schedule_attack
from my_bot import bot

from states import SetTime
from helper_functions import check_time

router = Router(name=__name__)


@router.message(SetTime.time, check_time)
async def change_time_for_habit(message: types.Message, state: FSMContext):
    """Changing time for habit"""
    data = await state.update_data(time=message.text)
    correct_time = data.get("time").split(":")
    await state.clear()
    await schedule_attack(
        name_habit=data.get("name_habit"),
        bot_father=bot,
        chat_idd=message.chat.id,
        hour=int(correct_time[0]),
        minute=int(correct_time[1]),
    )
    await message.answer(
        text=f"The notification time of your "
        f"{markdown.hbold(data.get('name_habit'))} habit has been changed.",
    )
