from pydantic import BaseModel


class StatusResponseSchema(BaseModel):
    status: bool = True
