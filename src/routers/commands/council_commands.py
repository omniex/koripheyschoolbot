from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from aiogram import Router, F

from src.Utils.database_methods import *
from src.Utils.keyboards import *
from src.Utils.messages import USERS_MENU_MESSAGE, START_MESSAGE_NOT_REGISTERED, START_MESSAGE_REGISTERED
from src.routers.commands.admin_commands import send_for_needed_users

router = Router(name=__name__)


class News(StatesGroup):
    for_who = State()
    news_text = State()


class Announcement(StatesGroup):
    for_who = State()
    wait_text = State()


@router.message(CommandStart(), F.from_user.id.in_(settings.council_ids))
async def handle_start(msg: types.Message, state: FSMContext):
    await state.clear()
    registered = await is_registered(msg)
    if registered:
        await msg.answer(START_MESSAGE_REGISTERED, reply_markup=ReplyKeyboardRemove())
        await handle_menu(msg)
    else:
        await msg.answer(START_MESSAGE_NOT_REGISTERED, reply_markup=ReplyKeyboardRemove())


@router.message(Command('menu'), F.from_user.id.in_(settings.council_ids))
async def handle_menu(msg: types.Message):
    await msg.answer(USERS_MENU_MESSAGE, reply_markup=await get_council_menu(msg.from_user.id),
                     parse_mode=ParseMode.MARKDOWN)


@router.message(Command('create_news'), F.from_user.id.in_(settings.council_ids))
async def handle_create_news(msg: types.Message, state: FSMContext):
    await msg.answer('Давайте начнём создание новости!')
    await msg.answer('Выберите для кого эта новость', reply_markup=await get_for_who_is_announcement_council())
    await state.set_state(News.for_who)


@router.message(News.for_who)
async def handle_for_who(msg: types.Message, state: FSMContext):
    await state.update_data(who=msg.text)
    data = await state.get_data()
    await msg.answer(f'Хорошо, только "{data["who"]}" увидит(-ят) эту новость. Теперь введите текст самой новости',
                     reply_markup=ReplyKeyboardRemove())
    await state.set_state(News.news_text)


@router.message(News.news_text)
async def handle_news_text(msg: types.Message, state: FSMContext):
    await state.update_data(information=msg.text)
    data = await state.get_data()
    for_who = await get_ids_for_send(data)
    await register_news(data)
    for user in for_who:
        await msg.bot.send_message(user, f'*ВНИМАНИЕ НОВОСТЬ*', parse_mode=ParseMode.MARKDOWN)
        await msg.copy_to(user, reply_markup=ReplyKeyboardRemove())
    await msg.answer('Новость успешно создана и отправлена!')
    await state.clear()


@router.message(Command('announcement'), F.from_user.id.in_(settings.council_ids))
async def handle_admin_announcement(msg: types.Message, state: FSMContext):
    await msg.answer('Выберите, кто должен увидеть это оповещение',
                     reply_markup=await get_for_who_is_announcement_council())
    await state.set_state(Announcement.for_who)


@router.message(Announcement.for_who)
async def handle_what_announcement(msg: types.Message, state: FSMContext):
    await state.update_data(who=msg.text)
    data = await state.get_data()
    await msg.answer(
        f'Хорошо, только "{data["who"]}" увидит(-ят) эту информацию. Теперь введите текст самого оповещения',
        reply_markup=ReplyKeyboardRemove())
    await state.set_state(Announcement.wait_text)


@router.message(Announcement.wait_text)
async def handle_announcement_text(msg: types.Message, state: FSMContext):
    await state.update_data(text=msg.text)
    data = await state.get_data()
    if data['who'] == '🫂Совет Гимназистов':
        await send_for_needed_users(msg, settings.council_ids, state)
    elif data['who'] == '👸Учителя':
        await send_for_needed_users(msg, settings.teacher_ids, state)
    elif data['who'] == 'Все пользователи':
        await send_for_needed_users(msg, settings.user_ids, state)
    else:
        await state.clear()
