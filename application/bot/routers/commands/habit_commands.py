from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from appeal_to_service import check_user_in_database
from states import User
from definer_commands import DEFINE_COMMAND

router = Router(name=__name__)

TEXT_ENTER_TOKEN = "Please enter your token."


@router.message(Command("create"))
async def command_create(message: types.Message, state: FSMContext):
    """Start Creating of user"""
    check_user = await check_user_in_database(idd=message.chat.id)
    if "detail" in check_user:
        await set_commands(command=message.text)
        await state.set_state(User.username)
        await message.answer(text="Hello my friend, what is your name?")
    else:
        await message.answer(text="You are already created.")


@router.message(Command("token"))
async def command_token(message: types.Message, state: FSMContext):
    """Start Getting token for user"""
    await set_commands(command=message.text)
    await state.set_state(User.username)
    await message.answer(text="Please enter your username.")


@router.message(Command("add_habit"))
async def command_add_habit(message: types.Message):
    """Start Adding a habit"""
    await set_commands(command=message.text)
    await message.answer(text=TEXT_ENTER_TOKEN)


@router.message(Command("get_habits"))
async def command_get_habits(message: types.Message):
    """Getting all habits in a database"""
    await set_commands(command=message.text)
    await message.answer(text=TEXT_ENTER_TOKEN)


@router.message(Command("edit_habit"))
async def command_edit_habit(message: types.Message):
    """Changing a habit"""
    await set_commands(command=message.text)
    await message.answer(text=TEXT_ENTER_TOKEN)


@router.message(Command("track_habit"))
async def command_track_habit(message: types.Message):
    """Fixation execution of a habit"""
    await set_commands(command=message.text)
    await message.answer(text=TEXT_ENTER_TOKEN)


@router.message(Command("habit_stats"))
async def command_habit_stats(message: types.Message):
    """Getting information about a habit from a database"""
    await set_commands(command=message.text)
    await message.answer(text=TEXT_ENTER_TOKEN)


@router.message(Command("set_reminder"))
async def command_set_reminder(message: types.Message):
    """Setting reminding of time for a habit"""
    await set_commands(command=message.text)
    await message.answer(text=TEXT_ENTER_TOKEN)


@router.message(Command("cancel"))
async def echo(
    message: types.Message,
    state: FSMContext,
):
    """Clearing state and dictionary"""
    await state.clear()
    DEFINE_COMMAND.clear()
    await message.answer(
        text="Your state has deleted and dictionary was cleared. Input any commands.",
    )


async def set_commands(command: str):
    DEFINE_COMMAND.clear()
    DEFINE_COMMAND[command.lstrip("/")] = True
