import emoji
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from appeal_to_service import check_token_for_user, get_habits_for_user
from diagrams import get_diagram
from keyboards.inline_keyboards import habits_kb

from definer_commands import DEFINE_COMMAND
from states import Habit


router = Router(name=__name__)


@router.message(F.text.func(len) == 185)
async def check_token_and_action(message: types.Message, state: FSMContext):
    """Checking a token and an action this habits"""
    token = await check_token_for_user(message.text)
    if "detail" not in token:
        if DEFINE_COMMAND.get("add_habit"):
            await state.set_state(Habit.name_habit)
            await message.answer(text="Please enter your name habit.")
        elif DEFINE_COMMAND.get("get_habits"):
            habits = await get_habits_for_user(message.chat.id)
            if "detail" not in habits:
                result = [
                    (
                        f"{markdown.hbold('Habit')}: {i['name_habit']}\n"
                        f"{markdown.hbold('Description')}: {i['description']}\n"
                        f"{markdown.hbold('Goal')}: {i['habit_goal']}\n"
                    )
                    for i in habits
                ]
                if result:
                    await message.answer(text="\n".join(result))
                else:
                    await message.answer(text="No have any habits.")
            else:
                await message.answer(text="User does not exist.")
        elif (
            DEFINE_COMMAND.get("edit_habit")
            or DEFINE_COMMAND.get("track_habit")
            or DEFINE_COMMAND.get("set_reminder")
        ):
            habits = await get_habits_for_user(message.chat.id)
            await message.answer(
                text="It is your habits:",
                reply_markup=habits_kb(habits),
            )
        else:
            habits = await get_habits_for_user(message.chat.id)
            path = await get_diagram(idd=message.chat.id, habits=habits)
            await message.bot.send_photo(
                chat_id=message.chat.id, photo=types.FSInputFile(path=path)
            )
    else:
        await message.answer(
            text=f"Your token's time is expired {emoji.emojize(':hourglass_done:')}"
        )
