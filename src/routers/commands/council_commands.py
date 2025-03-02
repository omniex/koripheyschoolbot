from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from src.Utils.database_methods import *
from src.Utils.keyboards import *

router = Router(name=__name__)


class News(StatesGroup):
    for_who = State()
    news_text = State()


@router.message(Command('create_news'))
async def handle_create_news(msg: types.Message, state: FSMContext):
    await msg.answer('Давайте начнём создание новости!')
    await msg.answer('Выберите для кого эта новость', reply_markup=await get_for_who_is_announcement())
    await state.set_state(News.for_who)


@router.message(News.for_who)
async def handle_for_who(msg: types.Message, state: FSMContext):
    await state.update_data(who=msg.text)
    data = await state.get_data()
    await msg.answer(f'Хорошо, только "{data["who"]}" увидит(-ят) эту новость. Теперь введите текст самой новости', reply_markup=ReplyKeyboardRemove())
    await state.set_state(News.news_text)


@router.message(News.news_text)
async def handle_news_text(msg: types.Message, state: FSMContext):
    await state.update_data(information=msg.text)
    data = await state.get_data()
    for_who = await get_ids_for_send(data)
    await register_news(data)
    for user in for_who:
        from src.main import bot
        await bot.send_message(user, f'*ВНИМАНИЕ НОВОСТЬ*\n\n*{data["information"]}*', parse_mode=ParseMode.MARKDOWN)
    await msg.answer('Новость успешно создана и отправлена!')
    await state.clear()
