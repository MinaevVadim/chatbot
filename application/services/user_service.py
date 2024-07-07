from sqlalchemy import select, cast, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from chatbot_logger import add_logger, decorator_main_logger
from models.user_models import User

from utils import hash_password

logger = add_logger(__name__)


@decorator_main_logger(logger)
async def get_user(session: AsyncSession, idd: int) -> User | None:
    """Getting a user"""
    stmt = select(User).where(User.telegram_id == cast(idd, Integer))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


@decorator_main_logger(logger)
async def user_create(session: AsyncSession, data: dict) -> None:
    """Creating a user"""
    username = data.get("username")
    telegram_id = data.get("telegram_id")
    password = data.get("password")
    session.add(
        User(
            username=username,
            telegram_id=telegram_id,
            password=hash_password(password=password),
        ),
    )
    await session.commit()
