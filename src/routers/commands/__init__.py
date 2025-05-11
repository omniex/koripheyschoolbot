__all__ = ("router", )

from aiogram import Router

from src.routers.commands.base_commands import router as base_commands_router
from src.routers.commands.student_commands import router as student_commands_router
from src.routers.commands.council_commands import router as council_commands_router
from src.routers.commands.admin_commands import router as admin_commands_router
from src.routers.commands.teacher_commands import router as teacher_commands_router
from src.routers.commands.registration_form import router as registration_router

router = Router()

router.include_routers(
    admin_commands_router,
    teacher_commands_router,
    council_commands_router,
    student_commands_router,
    base_commands_router,
    registration_router,
)