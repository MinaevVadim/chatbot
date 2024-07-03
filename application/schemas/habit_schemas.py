from datetime import datetime

from pydantic import BaseModel


class HabitUpdateSchema(BaseModel):
    name_habit: str = None
    description: str = None
    habit_goal: str = None


class HabitSchema(BaseModel):
    id: int = None
    telegram_id: int = None
    name_habit: str
    description: str
    habit_goal: str
    count: int = None
    alert_time: datetime = None
