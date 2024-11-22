from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.Utils.database_methods import get_all_users, execute_command, get_command, search_for_direct_user
from src.config import settings

router = Router(name=__name__)


class Search_class(StatesGroup):
    search_name = State()


@router.message(Command('users'), F.from_user.id.in_(settings.admin_ids))
async def handle_admin(msg: types.Message):
    await msg.reply('Hello admin')
    await msg.answer('Here is the list of all users: ')
    all_users = get_all_users()
    users_info = ''
    for user in all_users:
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\n'
    if users_info == '':
        await msg.answer('Nothing in database')
    else:
        await msg.answer(users_info)


@router.message(Command('database_exec'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    await msg.answer('Trying to execute the command')
    command = msg.text[15:]
    await msg.answer(f'command: {command}')
    try:
        execute_command(command)
    except Exception as e:
        await msg.answer(str(e))


@router.message(Command('database_get'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    await msg.answer('Trying to execute get command')
    command = msg.text[14:]
    await msg.answer(f'command: {command}')
    try:
        data = get_command(command)
        await msg.answer(f'Raw data: \n{data}')
    except Exception as e:
        await msg.answer(str(e))


@router.message(Command('search'), F.from_user.id.in_(settings.admin_ids))
async def search_user(msg: types.Message, state: FSMContext):
    await msg.answer('Пожалуйста, введите данные пользователя')
    await state.set_state(Search_class.search_name)


@router.message(Search_class.search_name)
async def handle_name(msg: types.Message, state: FSMContext):
    name = msg.text
    data = search_for_direct_user(name)
    await msg.answer(f'Вот, что мне удалось найти:')
    for user in data:
        users_info = ''
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\n'
        await msg.answer(users_info)
    await state.clear()
