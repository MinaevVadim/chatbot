from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from appeal_to_service import update_habits_for_user, add_habit_for_user
from config_schedule import schedule_attack

from definer_commands import DEFINE_COMMAND
from my_bot import bot

from states import Habit


router = Router(name=__name__)


@router.message(Habit.name_habit)
async def create_name_habit(message: types.Message, state: FSMContext):
    """Continue Adding a habit"""
    await state.update_data(name_habit=message.text)
    await state.set_state(Habit.description)
    await message.answer(text="Please enter your description.")


@router.message(Habit.description)
async def create_description_habit(message: types.Message, state: FSMContext):
    """Continue Adding a habit"""
    await state.update_data(description=message.text)
    await state.set_state(Habit.habit_goal)
    await message.answer(text="Please enter your habit goal.")


@router.message(Habit.habit_goal)
async def create_habit_goal_habit(message: types.Message, state: FSMContext):
    """Finish Adding a habit"""
    data = await state.update_data(habit_goal=message.text)
    if DEFINE_COMMAND.get("update_habit"):
        await state.update_data()
        await update_habits_for_user(DEFINE_COMMAND.get("id"), data)
        await state.clear()
        await message.answer(
            text="Your habit was changed.",
        )
    else:
        data.update(telegram_id=message.chat.id)
        await state.clear()
        await add_habit_for_user(dct=data)
        await schedule_attack(
            name_habit=data.get("name_habit"),
            bot_father=bot,
            chat_idd=message.chat.id,
        )
        await message.answer(
            text=f"It is your new habit: {markdown.hbold(data.get('name_habit'))}"
        )
