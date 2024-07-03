import emoji
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from appeal_to_service import (
    get_habits_for_user,
    get_habit_for_user,
    delete_habit_for_user,
    mark_habit_for_user,
)
from keyboards.inline_keyboards import (
    DeleteUpdateCBData,
    OptionsDeleteUpdate,
    habits_kb,
    HabitsCBData,
    update_or_delete_kb,
    execute_or_back_kb,
    DoneNotCompetedCBData,
    OptionsDoneNotCompleted,
)
from definer_commands import DEFINE_COMMAND
from states import SetTime, Habit
from helper_functions import check_date

router = Router(name=__name__)


@router.callback_query(DeleteUpdateCBData.filter(F.action == OptionsDeleteUpdate.root))
async def callback_back_to_habits(callback_query: CallbackQuery):
    """Back to habits"""
    habits = await get_habits_for_user(callback_query.message.chat.id)
    await callback_query.message.edit_text(
        text="It is your habits:",
        reply_markup=habits_kb(habits),
    )


@router.callback_query(HabitsCBData.filter())
async def callback_habit_kb(
    callback_query: CallbackQuery,
    callback_data: HabitsCBData,
    state: FSMContext,
):
    """Define an action this kb for habits"""
    habit = await get_habit_for_user(callback_data.id)
    if "detail" not in habit:
        if DEFINE_COMMAND.get("edit_habit"):
            message_text = markdown.text(
                emoji.emojize(":small_orange_diamond:") * 11,
                markdown.text(markdown.hbold("name: "), habit["name_habit"]),
                markdown.text(markdown.hbold("description: "), habit["description"]),
                markdown.text(markdown.hbold("goal: "), habit["habit_goal"]),
                sep="\n",
            )
            await callback_query.message.edit_text(
                text=message_text,
                reply_markup=update_or_delete_kb(callback_data.id),
                parse_mode=ParseMode.HTML,
            )
        elif DEFINE_COMMAND.get("set_reminder"):
            await state.set_state(SetTime.time)
            await state.update_data(name_habit=callback_data.name_habit)
            await callback_query.message.edit_text(
                text="What time do you wanna set for reminding"
                " of a habit in this format (hour:minutes): 15:30"
            )
        else:
            if DEFINE_COMMAND.get("track_habit"):
                await callback_query.message.edit_text(
                    text="Choose to perform or not to perform this habit.",
                    reply_markup=execute_or_back_kb(callback_data.id),
                )
    else:
        await callback_query.message.answer(text=habit.get("detail"))


@router.callback_query(
    DeleteUpdateCBData.filter(F.action == OptionsDeleteUpdate.update)
)
async def callback_update_habit(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
):
    """Updating a habit's parameters"""
    DEFINE_COMMAND.update(update_habit=True, id=callback_data.id)
    await state.set_state(Habit.name_habit)
    await callback_query.answer(
        text=f"If you don't want to change the data of "
        f"a habit, enter a minus sign: -",
        show_alert=True,
    )
    await callback_query.message.answer(text="Enter your new name habit.")


@router.callback_query(
    DeleteUpdateCBData.filter(F.action == OptionsDeleteUpdate.delete)
)
async def callback_delete_habit(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
):
    """Delete a habit"""
    await delete_habit_for_user(callback_data.id)
    await callback_query.message.answer(
        text="Your habit was deleted.",
    )
    habits = await get_habits_for_user(callback_query.message.chat.id)
    await callback_query.message.edit_text(
        text="It is your habits:",
        reply_markup=habits_kb(habits),
    )


@router.callback_query(
    DoneNotCompetedCBData.filter(F.action == OptionsDoneNotCompleted.done)
)
async def callback_done_habit(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
):
    """Count a habit"""
    habit = await get_habit_for_user(callback_data.id)
    if check_date(date=habit.get("alert_time")):
        habits = await get_habits_for_user(callback_query.message.chat.id)
        await mark_habit_for_user(callback_data.id)
        await callback_query.answer(
            text=f"Your habit was counted {emoji.emojize(':thumbs_up:')}",
            show_alert=True,
        )
        if habit.get("count") >= 21:
            await delete_habit_for_user(callback_data.id)
            await callback_query.message.answer(
                text=f"Congratulate my friend, you have performed the habit 21 days,"
                f" it was deleted from your list of habits {emoji.emojize(':star:')}"
            )
        await callback_query.message.edit_text(
            text="It is your habits:",
            reply_markup=habits_kb(habits),
        )
    else:
        await callback_query.answer(
            text="You cannot perform the habit more than once a day.",
            show_alert=True,
        )


@router.callback_query(
    DoneNotCompetedCBData.filter(F.action == OptionsDoneNotCompleted.not_completed)
)
async def callback_done_habit(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
):
    """Un count a habit"""
    await mark_habit_for_user(callback_data.id, extra=True)
    habits = await get_habits_for_user(callback_query.message.chat.id)
    await callback_query.answer(
        text="The number of completed habits has been reset,"
        " you will need to start all over again.",
        show_alert=True,
    )
    await callback_query.message.edit_text(
        text="It is your habits:",
        reply_markup=habits_kb(habits),
    )
