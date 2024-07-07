from datetime import datetime

from aiogram import types


def check_date(date: str) -> bool:
    """Function for checking date"""
    current_time = datetime.utcnow().timestamp()
    old_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
    return current_time - old_time > 86400


def check_time(message: types.Message):
    """Function for checking time"""
    return len(message.text) in (4, 5) and ":" in message.text
