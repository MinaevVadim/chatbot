from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_config.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    habits = relationship("Habit")

    def to_dict(self):
        return {"username": self.username, "telegram_id": self.telegram_id}
