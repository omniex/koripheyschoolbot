__all__ = ('router',)

from aiogram import Router

from src.routers.commands import router as commands_router
from src.routers.callback_handlers import router as callback_router

router = Router()

router.include_routers(
    callback_router,
    commands_router
)
