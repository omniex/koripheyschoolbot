from aiogram import Router
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command

from src.Utils.database_methods import get_all_users
from src.config import settings

router = Router(name=__name__)


@router.message(Command('announcement'), F.from_user.id.in_(settings.teacher_ids))
async def handle_announcement(msg: types.Message):
    text = msg.text[14:]
    user_list = get_all_users()
    for user in user_list:
        await msg.bot.send_message(user[7], text, parse_mode=ParseMode.HTML)