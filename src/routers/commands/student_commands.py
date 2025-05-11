from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.Utils.database_methods import *
from src.Utils.keyboards import *

router = Router(name=__name__)


class SearchUser(StatesGroup):
    search_name = State()
    send_message = State()


# @router.message()
# async def handle_direct(msg: types.Message, state: FSMContext):
#     await msg.answer('Введите имя/фамилию человека, которому хотите отправить сообщение'
#                      'Вам будет показан данный пользователь'
#                      'Нажмите на галочку, если это тот, кому вы хотите отправить сообщение')
#     await state.set_state(SearchUser.search)
#

# @router.message(Command('direct'))
# async def search_user(msg: types.Message, state: FSMContext):
#     # args = msg.text.split()
#     # if len(args) > 1:
#     #     await msg.answer('Command using: /search')
#     #     return
#     await msg.answer('Введите имя/фамилию пользователя')
#     await state.set_state(SearchUser.search_name)
#
#
# @router.message(SearchUser.search_name)
# async def search_for_user(msg: types.Message, state: FSMContext):
#     name = msg.text
#     data = await search_for_direct_data('users', 'USERS', name)
#     await msg.answer(f'Вот, что мне удалось найти:', reply_markup=await search_for_users_kb(data))
#     await state.set_state(SearchUser.send_message)
#     # for user in data:
#     #     users_info = ''
#     #     users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\n\n'
#     #     await msg.answer(users_info)