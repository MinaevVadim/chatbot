from typing import Any, Annotated
from fastapi.exceptions import HTTPException
from fastapi import Depends
from starlette import status
from jwt.exceptions import InvalidTokenError

from services.user_service import get_user
from schemas.user_schemas import UserSchema
from models.user_models import User
from utils import validate_password, decode_jwt
from db_config.db import async_session


async def db():
    async with async_session() as session:
        yield session


async def check_auth_user(
    data: UserSchema,
    session: Annotated[Any, Depends(db)],
) -> User:
    user_data = dict(data)
    user = await get_user(session=session, idd=user_data.get("telegram_id"))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesnt exist in a database.",
        )
    if user.username != user_data.get("username"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is not correct.",
        )
    if not validate_password(user_data.get("password"), user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is not correct.",
        )
    return user


async def check_user_by_token(
    token: str,
    session: Annotated[Any, Depends(db)],
) -> User:
    try:
        payload = decode_jwt(token=str(token))
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid."
        )
    user = await get_user(session=session, idd=payload.get("telegram_id"))
    if user.telegram_id != payload.get("telegram_id"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not correct.",
        )
    return user
