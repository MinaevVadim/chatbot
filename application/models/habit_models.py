from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_config.db import Base


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_habit: Mapped[str]
    description: Mapped[str]
    habit_goal: Mapped[str]
    user: Mapped[id] = mapped_column(ForeignKey("users.id"))

    habit_tracking = relationship(
        "HabitTracking",
        uselist=False,
        cascade="all,delete",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name_habit": self.name_habit,
            "description": self.description,
            "habit_goal": self.habit_goal,
            "count": self.habit_tracking.count,
            "alert_time": self.habit_tracking.alert_time,
        }


class HabitTracking(Base):
    __tablename__ = "habittrackings"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_time: Mapped[datetime] = mapped_column(default=func.now())
    count: Mapped[int] = mapped_column(default=0)
    habit: Mapped[id] = mapped_column(ForeignKey("habits.id"), unique=True)
