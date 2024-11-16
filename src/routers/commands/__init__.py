__all__ = ("router", )

from aiogram import Router

from .base_commands import router as base_commands_router
from .student_commands import router as student_commands_router
from .moderation_commands import router as moderation_commands_router
from .admin_commands import router as admin_commands_router
from .teacher_commands import router as teacher_commands_router

router = Router()

router.include_routers(base_commands_router,
                       student_commands_router,
                       teacher_commands_router,
                       moderation_commands_router,
                       admin_commands_router,
                       )