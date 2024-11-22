from aiogram import Router

from .apply_information_kb_callback_handlers import router as change_kb_callback_router

router = Router(name=__name__)

router.include_routers(change_kb_callback_router)