from typing import Annotated, Any
from fastapi import Depends, APIRouter
from starlette import status

from chatbot_logger import add_logger
from dependencies import db

from schemas.habit_schemas import HabitSchema, HabitUpdateSchema
from schemas.status_schemas import StatusResponseSchema

from services.habit_service import (
    add_new_habit,
    get_all_habits,
    get_a_one_habit,
    update_habit,
    delete_a_one_habit,
    track_habit,
)
from utils import obj_does_not_exist

router = APIRouter(prefix="/habit", tags=["habits"])

logger = add_logger(__name__)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=StatusResponseSchema,
)
async def add_habit(
    data: HabitSchema,
    session: Annotated[Any, Depends(db)],
):
    habit = await add_new_habit(session=session, data=dict(data))
    if habit is None:
        obj_does_not_exist("User")
    return StatusResponseSchema(status=True)


@router.get(
    "/user/{telegram_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[HabitSchema],
)
async def get_habits(
    telegram_id: int,
    session: Annotated[Any, Depends(db)],
):
    habits = await get_all_habits(session=session, idd=telegram_id)
    if habits is None:
        obj_does_not_exist("Habit")
    return habits


@router.get(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=HabitSchema,
)
async def get_habit(
    idd: int,
    session: Annotated[Any, Depends(db)],
):
    habit = await get_a_one_habit(session=session, idd=idd)
    if habit:
        return habit.to_dict()
    obj_does_not_exist("Habit")


@router.patch(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=StatusResponseSchema,
)
async def habit_update(
    data: HabitUpdateSchema,
    idd: int,
    session: Annotated[Any, Depends(db)],
):
    habit = await update_habit(session=session, idd=idd, data=dict(data))
    if habit is None:
        obj_does_not_exist("Habit")
    return StatusResponseSchema(status=True)


@router.delete(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=StatusResponseSchema,
)
async def delete_habit(
    idd: int,
    session: Annotated[Any, Depends(db)],
):
    habit = await delete_a_one_habit(session=session, idd=idd)
    if not habit:
        obj_does_not_exist("Habit")
    return StatusResponseSchema(status=True)


@router.post(
    "/{idd}",
    status_code=status.HTTP_200_OK,
    response_model=StatusResponseSchema,
)
async def mark_habit(
    idd: int,
    session: Annotated[Any, Depends(db)],
    extra: bool = None,
):
    if extra:
        habit = await track_habit(session=session, idd=idd, extra=extra)
    else:
        habit = await track_habit(session=session, idd=idd)
    if not habit:
        obj_does_not_exist("Habit")
    return StatusResponseSchema(status=True)
