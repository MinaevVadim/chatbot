from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
import emoji
from appeal_to_service import create_new_user, get_token_for_user
from definer_commands import DEFINE_COMMAND

from states import User

router = Router(name=__name__)


@router.message(User.username)
async def username_create_or_get_token(message: types.Message, state: FSMContext):
    """Continue Creating of user"""
    await state.update_data(username=message.text)
    await state.set_state(User.password)
    await message.answer(text="Please enter your password.")


@router.message(User.password)
async def password_create_or_get_token(message: types.Message, state: FSMContext):
    """Finish Creating of user"""
    data = await state.update_data(password=message.text)
    await message.delete()
    await state.clear()
    dct = {
        "username": data.get("username"),
        "telegram_id": message.chat.id,
        "password": data.get("password"),
    }
    if DEFINE_COMMAND.get("create"):
        await create_new_user(dct=dct)
        await message.answer(
            text=f"Thanks for registration, {markdown.hbold(data.get('username'))}. "
            f"Next create your new token /token"
        )
    else:
        token = await get_token_for_user(dct=dct)
        if "detail" in token:
            await message.answer(text=token.get("detail"))
        else:
            await message.answer(
                text=f"It is your new token {emoji.emojize(':down_arrow:')}"
            )
            await message.answer(text=token.get("access_token"))
