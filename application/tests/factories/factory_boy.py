from asyncio import current_task
from datetime import datetime

import factory
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    async_scoped_session,
)

from models.habit_models import Habit, HabitTracking
from models.user_models import User
from env_config import settings as stg
from utils import hash_password


class MyEngine:
    def __init__(self) -> None:
        self.path = f"postgresql+asyncpg://{stg.db_user}:{stg.db_pass}@db/test"
        self.engine = create_async_engine(
            self.path,
            poolclass=NullPool,
        )

    def async_session(self):
        return async_scoped_session(
            async_sessionmaker(
                self.engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            scopefunc=current_task,
        )


my_engine = MyEngine()
engine = my_engine.engine
session = my_engine.async_session()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    telegram_id = factory.Sequence(lambda n: n + 10)
    username = factory.Sequence(lambda n: "User %d" % n)
    password = hash_password("qwery")
    is_active = factory.Faker("random_element", elements=[True, False])


class HabitFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Habit
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    name_habit = factory.Sequence(lambda n: "Habit %d" % n)
    description = factory.Faker("sentence", nb_words=10)
    habit_goal = factory.Faker("sentence", nb_words=10)

    user = factory.SubFactory(UserFactory)


class HabitTrackingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HabitTracking
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n + 1)
    count = factory.Faker("random_number")

    habit = factory.SubFactory(HabitFactory)
