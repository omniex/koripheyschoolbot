from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.Utils.database_methods import register_user, get_all
from src.Utils.messages import INFO_MESSAGE
from src.routers.commands.admin_commands import *
from src.routers.commands.base_commands import handle_news, handle_report
from src.routers.commands.registration_form import User
from src.routers.commands.council_commands import *

router = Router(name=__name__)


@router.callback_query(F.data == 'btn_notes')
async def handle_notes(callback_query: CallbackQuery):
    await callback_query.answer()
    pass


@router.callback_query(F.data == 'btn_schedule')
async def handle_schedule(callback_query: CallbackQuery):
    await callback_query.answer()
    pass


@router.callback_query(F.data == 'btn_direct')
async def handle_direct(callback_query: CallbackQuery):
    await callback_query.answer()
    pass


@router.callback_query(F.data == 'btn_info')
async def handle_info(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(INFO_MESSAGE)


@router.callback_query(F.data == 'btn_search_user')
async def handle_search(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await search_user(callback_query.message, state)


@router.callback_query(F.data == 'btn_list_users')
async def handle_list_users(callback_query: CallbackQuery):
    await callback_query.answer()
    await handle_user_list(callback_query.message)


@router.callback_query(lambda c: c.data.startswith("btn_get_news:"))
async def handle_get_news(callback_query: CallbackQuery):
    await callback_query.answer()
    user_id = int(callback_query.data.split(":")[1])
    await handle_news(callback_query.message, user_id)


@router.callback_query(F.data == 'btn_make_news')
async def handle_get_news(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await handle_create_news(callback_query.message, state)


@router.callback_query(F.data == 'btn_send_announcement')
async def handle_send_announcement(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await handle_admin_announcement(callback_query.message, state)


@router.callback_query(F.data == 'btn_tickets_list')
async def handle_ticket_list(callback_query: CallbackQuery):
    await callback_query.answer()
    await handle_reports(callback_query.message)


@router.callback_query(F.data == 'btn_food')
async def handle_food_poll(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await handle_food(callback_query.message, state)


@router.callback_query(lambda c: c.data.startswith("btn_create_ticket:"))
async def handle_create_ticket(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    user_id = int(callback_query.data.split(":")[1])
    await handle_report(callback_query.message, state, user_id=user_id)
