__all__ = ("router",)

from aiogram import Router

from .user_hadlers import router as user_router
from .habit_handlers import router as habit_router
from .token_handlers import router as token_router
from .schedule_time_handlers import router as schedule_router
from .commands import router as commands_router
from .callback_handlers import router as callback_router

router = Router(name=__name__)

router.include_router(user_router)
router.include_router(habit_router)
router.include_router(token_router)
router.include_router(schedule_router)
router.include_router(callback_router)
router.include_router(commands_router)
