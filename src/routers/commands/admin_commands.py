from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.Utils.database_methods import execute_command, get_command, \
    create_db_food, register_meal, get_all, search_for_direct_data
from src.config import settings

from src.Utils.keyboards import get_food_marks, get_meal

router = Router(name=__name__)


class Search_class(StatesGroup):
    search_name = State()


class FoodSurvey(StatesGroup):
    waiting_for_answer = State()
    what_meal = State()
    meal = ''
    need = 0
    msg_con: types.Message
    state_con: FSMContext


@router.message(Command('users'), F.from_user.id.in_(settings.admin_ids))
async def handle_admin(msg: types.Message):
    await msg.reply('Hello admin')
    await msg.answer('Here is the list of all users: ')
    all_users = get_all('users', 'USERS')
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
async def search_user(msg: types.Message):
    name = msg.text[8:]
    data = search_for_direct_data('users', 'USERS', name)
    print(f'args {name}')
    await msg.answer(f'Вот, что мне удалось найти:')
    for user in data:
        users_info = ''
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\n'
        await msg.answer(users_info)


#old method of search
# @router.message(Search_class.search_name)
# async def handle_name(msg: types.Message, state: FSMContext):
#     name = msg.text
#     data = search_for_direct_data('users', 'USERS'name)
#     await msg.answer(f'Вот, что мне удалось найти:')
#     for user in data:
#         users_info = ''
#         users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\n'
#         await msg.answer(users_info)
#     await state.clear()

@router.message(Command('food'), F.from_user.id.in_(settings.admin_ids))
async def handle_food(msg: types.Message, state: FSMContext):
    create_db_food()
    arr = msg.text.split()

    if len(arr) < 2 or not arr[1].isdigit():
        await msg.answer("Использование: /food <количество>")
        return

    FoodSurvey.need = int(arr[1])
    FoodSurvey.msg_con = msg
    FoodSurvey.state_con = state

    await msg.answer("Какой это приём пищи?", reply_markup=get_meal())
    await state.set_state(FoodSurvey.what_meal)


@router.message(FoodSurvey.what_meal)
async def handle_meal(msg: types.Message, state: FSMContext):
    await msg.answer(f'Начинаю опрос из {FoodSurvey.need} вопросов.')
    await state.update_data(remaining=FoodSurvey.need, good=0, bad=0, meal=msg.text)
    await ask_question(FoodSurvey.msg_con, FoodSurvey.state_con)


async def ask_question(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    remaining = data.get("remaining", 0)

    if remaining <= 0:
        good = data.get("good", 0)
        bad = data.get("bad", 0)
        meal = data.get("meal", 'None')
        await msg.answer(
            f'Приём пищи: {meal}\nВсего ответов: {good + bad}\n✅ Понравилось: {good}\n❌ Не понравилось: {bad}')
        register_meal(data)
        await state.clear()
        return

    await msg.answer(f'Обрабатываю ответ - {remaining}', reply_markup=get_food_marks())
    await state.set_state(FoodSurvey.waiting_for_answer)


@router.message(FoodSurvey.waiting_for_answer)
async def handle_answer(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    remaining = data.get("remaining", 0)
    good = data.get("good", 0)
    bad = data.get("bad", 0)

    if msg.text == '✅Мне всё понравилось':
        good += 1
    elif msg.text == '❌Мне не понравилось':
        bad += 1
    elif msg.text == 'Остановить':
        await state.update_data(remaining=0, good=good, bad=bad)
        await ask_question(msg, state)
        return
    else:
        await msg.answer("Неправильный ответ, выбери вариант из кнопок.")
        return

    await state.update_data(remaining=remaining - 1, good=good, bad=bad)
    await ask_question(msg, state)
