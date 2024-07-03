from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    telegram_id: int
    password: str


class UserResponsesSchema(BaseModel):
    username: str
    telegram_id: int
