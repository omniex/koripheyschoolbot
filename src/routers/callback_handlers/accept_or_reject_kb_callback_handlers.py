from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.Utils.database_methods import change_status

router = Router(name=__name__)


@router.callback_query(lambda c: c.data.startswith("btn_approve:"))
async def handle_approve(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    user_id = int(callback_query.data.split(":")[1])
    await change_status(user_id, 'approved', callback_query.message)
    await callback_query.answer("Заявка одобрена! ✅")
    from src.main import bot
    await bot.send_message(user_id, "Ваша заявка одобрена! 🎉")


@router.callback_query(lambda c: c.data.startswith("btn_reject:"))
async def handle_approve(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    user_id = int(callback_query.data.split(":")[1])
    await change_status(user_id, 'rejected', callback_query.message)
    await callback_query.answer("Заявка отклонена! ❌")
    from src.main import bot
    await bot.send_message(user_id, "Ваша заявка отклонена! ❌")