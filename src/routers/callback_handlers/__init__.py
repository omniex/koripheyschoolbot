__all__ = ('router',)
from aiogram import Router

from src.routers.callback_handlers.apply_information_kb_callback_handlers import router as change_kb_callback_router
from src.routers.callback_handlers.accept_or_reject_kb_callback_handlers import router as accept_or_reject_router
from src.routers.callback_handlers.menu_kb_callback_handlers import router as menu_kb_callback_router
from src.routers.callback_handlers.complete_or_not_kb_callback_handlers import router as complete_information_router

router = Router(name=__name__)

router.include_routers(change_kb_callback_router,
                       accept_or_reject_router,
                       menu_kb_callback_router,
                       complete_information_router)