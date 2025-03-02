from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.Utils.database_methods import register_user, get_all, change_status_ticket
from src.routers.commands.registration_form import User

router = Router(name=__name__)


@router.callback_query(lambda c: c.data.startswith("btn_completed:"))
async def handle_completed(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    ticket_id = callback_query.data.split(":")[1]
    await change_status_ticket(ticket_id, 'completed', callback_query.message)
    await callback_query.answer("Заявка выполнена! ✅")
    from src.main import bot
    await bot.send_message(ticket_id.split('_')[0], "Ваша заявка выполнена! ✅")


@router.callback_query(lambda c: c.data.startswith("btn_in_work:"))
async def handle_completed(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    ticket_id = callback_query.data.split(":")[1]
    await change_status_ticket(ticket_id, 'in work', callback_query.message)
    await callback_query.answer("Заявка взята в работу! 🛠️")
    from src.main import bot
    await bot.send_message(ticket_id.split('_')[0], "Ваша заявка взята в работу! 🛠️")


@router.callback_query(lambda c: c.data.startswith("btn_not_completed:"))
async def handle_completed(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    ticket_id = callback_query.data.split(":")[1]
    await change_status_ticket(ticket_id, 'rejected', callback_query.message)
    await callback_query.answer("Заявка отклонена! ❌")
    from src.main import bot
    await bot.send_message(ticket_id.split('_')[0], "Ваша заявка отклонена! ❌")
