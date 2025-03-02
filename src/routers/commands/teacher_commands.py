from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from src.Utils.database_methods import *
from src.Utils.keyboards import *
from src.config import settings

router = Router(name=__name__)


@router.message(Command('announcement'), F.from_user.id.in_(settings.teacher_ids))
async def handle_admin_announcement(msg: types.Message):
    text = msg.text[14:]
    await msg.answer('Выберите, кто должен увидеть это оповещение', reply_markup=await get_for_who_is_announcement())
    for user in user_list:
        await msg.bot.send_message(user[7], text, parse_mode=ParseMode.HTML)