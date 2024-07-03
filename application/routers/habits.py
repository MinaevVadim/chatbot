from typing import Annotated, Any
from fastapi.exceptions import HTTPException
from fastapi import Depends, APIRouter
from starlette import status

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

router = APIRouter(prefix="/habit", tags=["habits"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=StatusResponseSchema,
)
async def add_habit(
    data: HabitSchema,
    session: Annotated[Any, Depends(db)],
):
    await add_new_habit(session=session, data=dict(data))
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
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Habit does not exist.",
    )


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
    await update_habit(session=session, idd=idd, data=dict(data))
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
    await delete_a_one_habit(session=session, idd=idd)
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
        await track_habit(session=session, idd=idd, extra=extra)
    else:
        await track_habit(session=session, idd=idd)
    return StatusResponseSchema(status=True)
