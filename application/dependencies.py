import inspect
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

from chatbot_logger import add_logger, decorator_main_logger

logger = add_logger(__name__)


async def db():
    async with async_session() as session:
        yield session


@decorator_main_logger(logger)
async def check_auth_user(
    data: UserSchema,
    session: Annotated[Any, Depends(db)],
) -> User:
    """Checking the user for existence in the database"""
    user_data = dict(data)
    user = await get_user(session=session, idd=user_data.get("telegram_id"))
    if user is None:
        text = "User doesnt exist in a database."
        logger.error(text)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=text,
        )
    if user.username != user_data.get("username"):
        text = "Username is not correct."
        logger.error(text)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=text,
        )
    if not validate_password(user_data.get("password"), user.password):
        text = "Password is not correct."
        logger.error(text)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=text,
        )
    return user


@decorator_main_logger(logger)
async def check_user_by_token(
    token: str,
    session: Annotated[Any, Depends(db)],
) -> User:
    """Checking the user for existence in the database by token"""
    try:
        payload = decode_jwt(token=str(token))
    except InvalidTokenError as exc:
        logger.exception(f"Token was expired, {exc}, func: {inspect.stack()[0][3]}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not valid.",
        )
    user = await get_user(session=session, idd=payload.get("telegram_id"))
    if user.telegram_id != payload.get("telegram_id"):
        text = "User is not correct."
        logger.error(text)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=text,
        )
    return user
