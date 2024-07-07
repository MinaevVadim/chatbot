import logging
from functools import wraps
from typing import Any, Callable


def add_logger(name: Any) -> logging.Logger:
    """Custom logger"""
    logger = logging.getLogger(name)
    handler_logger = logging.FileHandler(filename="chatbot.log")
    logger.addHandler(handler_logger)
    logger.setLevel("DEBUG")
    formatter_logger = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler_logger.setFormatter(formatter_logger)
    return logger


def decorator_main_logger(my_logger: logging.Logger) -> Callable:
    def decorator_logger(func: Callable) -> Callable:
        """Logger for information and control about working functions"""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            my_logger.debug(f"Start working of a func: {func.__name__}")
            result = await func(*args, **kwargs)
            my_logger.debug(f"Finish working of a func: {func.__name__}")
            return result

        return wrapper

    return decorator_logger
