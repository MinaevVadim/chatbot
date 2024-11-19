import datetime

import bcrypt
import jwt
from fastapi import HTTPException
from starlette import status

from env_config import settings


def encode_jwt(
    payload: dict,
    key=settings.secret_key,
    algorithm="HS256",
) -> str:
    """Create a jwt"""
    time = datetime.datetime.utcnow()
    payload.update(iat=time, exp=time + datetime.timedelta(minutes=30))
    return jwt.encode(payload, key, algorithm)


def decode_jwt(
    token: str,
    key=settings.secret_key,
    algorithms="HS256",
) -> dict:
    """Getting a jwt"""
    return jwt.decode(token, key, algorithms)


def hash_password(password: str) -> bytes:
    """Hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    """Validate password"""
    return bcrypt.checkpw(password.encode(), hashed_password)


def obj_does_not_exist(obj: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{obj} does not exist.",
    )
