__all__ = ("router", )

from aiogram import Router

from src.routers.commands.base_commands import router as base_commands_router
from src.routers.commands.student_commands import router as student_commands_router
from src.routers.commands.council_commands import router as moderation_commands_router
from src.routers.commands.admin_commands import router as admin_commands_router
from src.routers.commands.teacher_commands import router as teacher_commands_router

router = Router()

router.include_routers(base_commands_router,
                       student_commands_router,
                       teacher_commands_router,
                       moderation_commands_router,
                       admin_commands_router,
                       )