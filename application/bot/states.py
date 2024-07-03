from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    username = State()
    password = State()


class Habit(StatesGroup):
    telegram_id = State()
    name_habit = State()
    description = State()
    habit_goal = State()


class SetTime(StatesGroup):
    time = State()
    name_habit = State()
