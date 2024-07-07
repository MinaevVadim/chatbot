import os
import sys
from datetime import datetime

from aiogram import types

sys.path.append(os.path.join(os.getcwd()))
from chatbot_logger import add_logger

logger = add_logger(__name__)


def check_date(date: str) -> bool:
    """Function for checking date"""
    current_time = datetime.utcnow().timestamp()
    old_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").timestamp()
    return current_time - old_time > 86400


def check_time(message: types.Message):
    """Function for checking time"""
    return len(message.text) in (4, 5) and ":" in message.text
