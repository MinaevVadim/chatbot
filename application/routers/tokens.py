from typing import Annotated, Any
from fastapi import Depends, APIRouter
from starlette import status

from dependencies import check_auth_user, check_user_by_token

from schemas.status_schemas import StatusResponseSchema
from schemas.token_schemas import TokenSchema

from utils import encode_jwt

router = APIRouter(prefix="/token", tags=["tokens"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenSchema,
)
async def get_token(
    user: Annotated[Any, Depends(check_auth_user)],
):
    payload = {
        "telegram_id": user.telegram_id,
        "username": user.username,
    }
    token = encode_jwt(payload=payload)
    return TokenSchema(
        access_token=token,
        type="bearer",
    )


@router.get(
    "/{token}",
    status_code=status.HTTP_200_OK,
    response_model=StatusResponseSchema,
)
async def check_token(
    user: Annotated[Any, Depends(check_user_by_token)],
):
    return StatusResponseSchema(status=True)
