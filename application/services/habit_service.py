import datetime
from typing import Any

from sqlalchemy import select, Cast, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from starlette import status

from chatbot_logger import add_logger, decorator_main_logger
from models.user_models import User

from models.habit_models import HabitTracking

from models.habit_models import Habit

logger = add_logger(__name__)


@decorator_main_logger(logger)
async def add_new_habit(session: AsyncSession, data: dict) -> bool | None:
    """Create a new habit"""
    result = await session.execute(
        select(User).where(User.telegram_id == Cast(data.get("telegram_id"), Integer))
    )
    user = result.scalar_one_or_none()
    if not user:
        return
    new_habit = Habit(
        name_habit=data.get("name_habit"),
        description=data.get("description"),
        habit_goal=data.get("habit_goal"),
        user=user.id,
    )
    session.add(new_habit)
    await session.flush()
    session.add(HabitTracking(habit=new_habit.id))
    await session.commit()
    return True


@decorator_main_logger(logger)
async def get_all_habits(session: AsyncSession, idd: int) -> list | None:
    """Getting all habits"""
    user = await session.execute(select(User).where(User.telegram_id == idd))
    user = user.scalar_one_or_none()
    if user is None:
        return
    stmt = (
        select(Habit)
        .options(joinedload(Habit.habit_tracking))
        .where(Habit.user == user.id)
    )
    result = await session.execute(stmt)
    lst = []
    for i in result.unique().scalars().all():
        dct = {
            "id": i.id,
            "telegram_id": idd,
            "name_habit": i.name_habit,
            "description": i.description,
            "habit_goal": i.habit_goal,
            "count": i.habit_tracking.count,
        }
        lst.append(dct)
    return lst


@decorator_main_logger(logger)
async def get_habit(session: AsyncSession, idd: int) -> Any:
    """Getting a one habit"""
    obj = await session.execute(
        select(Habit).options(joinedload(Habit.habit_tracking)).where(Habit.id == idd)
    )
    obj = obj.scalar_one_or_none()
    return obj


@decorator_main_logger(logger)
async def get_a_one_habit(session: AsyncSession, idd: int) -> Any:
    """Helper getting a one habit"""
    obj = await get_habit(session=session, idd=idd)
    return obj


@decorator_main_logger(logger)
async def update_habit(session: AsyncSession, idd: int, data: dict) -> None | bool:
    """Updating a habit"""
    obj = await get_habit(session=session, idd=idd)
    if obj is None:
        return
    for key, value in data.items():
        if value == "-":
            continue
        setattr(obj, key, value)
    await session.commit()
    return True


@decorator_main_logger(logger)
async def delete_a_one_habit(session: AsyncSession, idd: int) -> None | bool:
    """Delete a habit"""
    obj = await get_habit(session=session, idd=idd)
    if not obj:
        return
    await session.delete(obj)
    await session.commit()
    return True


@decorator_main_logger(logger)
async def track_habit(session: AsyncSession, idd: int, extra=False) -> None | bool:
    """Mark or reset count of a habit"""
    obj = await get_habit(session=session, idd=idd)
    if not obj:
        return
    habit_track = await session.execute(
        select(HabitTracking).where(HabitTracking.habit == Cast(obj.id, Integer))
    )
    habit = habit_track.scalar_one_or_none()
    habit.alert_time = datetime.datetime.utcnow()
    if extra:
        habit.count = 0
    else:
        habit.count += 1
    await session.commit()
    return True
