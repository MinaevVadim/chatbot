from typing import Annotated, Any
from fastapi.exceptions import HTTPException
from fastapi import Depends, APIRouter
from starlette import status

from dependencies import db

from schemas.status_schemas import StatusResponseSchema
from schemas.user_schemas import UserResponsesSchema, UserSchema

from services.user_service import get_user, user_create


router = APIRouter(prefix="/user", tags=["users"])


@router.get(
    path="/{telegram_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponsesSchema,
)
async def user_get(
    telegram_id: int,
    session: Annotated[Any, Depends(db)],
):
    user = await get_user(session=session, idd=telegram_id)
    if user:
        return user.to_dict()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User does not exist.",
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=StatusResponseSchema,
)
async def create_user(
    data: UserSchema,
    session: Annotated[Any, Depends(db)],
):
    await user_create(session=session, data=dict(data))
    return StatusResponseSchema(status=True)
