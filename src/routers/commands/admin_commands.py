from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command

from src.Utils.database_methods import get_all_users, execute_command
from src.config import settings

router = Router(name=__name__)


@router.message(Command('users'), F.from_user.id.in_(settings.admin_ids))
async def handle_admin(msg: types.Message):
    await msg.reply('Hello admin')
    await msg.answer('Here is the list of all users: ')
    all_users = get_all_users()
    users_info = ''
    for user in all_users:
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: {user[6]}\n Id: {user[7]}\n'
    if users_info == '':
        await msg.answer('Nothing in database')
    else:
        await msg.answer(users_info)


@router.message(Command('database'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    await msg.answer('Trying to execute the command')
    command = msg.text[10:]
    await msg.answer(f'command: {command}')
    try:
        execute_command(command)
    except Exception as e:
        await msg.answer(str(e))

