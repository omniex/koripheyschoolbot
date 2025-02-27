import os

from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from src.Utils.database_methods import *
# execute_command, get_command, \
#     create_db_food, register_meal, get_all, search_for_direct_data, export_to_excel
from src.config import settings

from src.Utils.keyboards import *

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


class Announcement(StatesGroup):
    for_who = State()
    wait_text = State()


@router.message(Command('users'), F.from_user.id.in_(settings.admin_ids))
async def handle_admin(msg: types.Message):
    await msg.reply('Hello admin')
    await msg.answer('Here is the list of all users: ')
    all_users = get_all('users', 'USERS')
    users_info = ''
    for user in all_users:
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\nRole: {user[8]}\n\n'
    if users_info == '':
        await msg.answer('Nothing in database')
    else:
        await msg.answer(users_info)


@router.message(Command('database_exec'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    args = msg.text.split()
    if len(args) < 3:
        await msg.answer('Command using: /database_exec <database name> <command>')
        return
    ind = len(f'{args[0]} {args[1]}')
    await msg.answer(f'Trying to execute command: {msg.text[ind:]}')
    try:
        execute_command(msg.text[ind:], args[1])
    except Exception as e:
        await msg.answer(str(e))


@router.message(Command('database_get'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    args = msg.text.split()
    if len(args) < 3:
        await msg.answer('Command using: /database_get <database name> <command>')
        return
    ind = len(f'{args[0]} {args[1]}')
    await msg.answer(f'Trying to execute command: {msg.text[ind:]}')
    try:
        data = get_command(msg.text[ind:], args[1])
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
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\n\n'
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
            f'Приём пищи: {meal}\nВсего ответов: {good + bad}\nПроцент понравившихся: {good / (good + bad) * 100}%\n✅ Понравилось: {good}\n❌ Не понравилось: {bad}')
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


@router.message(Command('export_excel'), F.from_user.id.in_(settings.admin_ids))
async def handle_excel(msg: types.Message, state: FSMContext):
    args = msg.text.split()
    if len(args) != 3:
        await msg.answer('Command using: /export_excel <database name> <table name>')
        return
    try:
        export_to_excel(args[1], args[2])
        await msg.answer_document(FSInputFile(f'{args[2]}.xlsx'))
        os.remove(f'{args[2]}.xlsx')
    except Exception as e:
        print(e)


@router.message(Command('change_role'), F.from_user.id.in_(settings.admin_ids))
async def handle_changing_role(msg: types.Message):
    args = msg.text.split()
    if len(args) != 3:
        await msg.answer('Command using: /change_role <user_id> <new_role>')
        return

    if args[2] == 'admin':
        await msg.answer('Nobody can give admin role, you need to add it manually in code')

    try:
        await change_role(int(args[1]), args[2], msg)
    except Exception as e:
        print(e)


@router.message(Command('announcement'), F.from_user.id.in_(settings.admin_ids))
async def handle_admin_announcement(msg: types.Message, state: FSMContext):
    await msg.answer('Выберите, кто должен увидеть это оповещение', reply_markup=get_for_who_is_annoucement())
    await state.set_state(Announcement.for_who)


@router.message(Announcement.for_who)
async def handle_what_announcement(msg: types.Message, state: FSMContext):
    await state.update_data(who=msg.text)
    data = await state.get_data()
    await msg.answer(f'Хорошо, только "{data["who"]}" увидит(-ят) эту информацию. Теперь введите текст самого оповещения')
    await state.set_state(Announcement.wait_text)


@router.message(Announcement.wait_text)
async def handle_announcement_text(msg: types.Message, state: FSMContext):
    await state.update_data(text=msg.text)
    data = await state.get_data()
    if data['who'] == '🥷Администрация':
        await send_for_needed_users(data["text"], msg, settings.admin_ids, state)
    elif data['who'] == '🫂Совет Гимназистов':
        await send_for_needed_users(data["text"], msg, settings.council_ids, state)
    elif data['who'] == '👸Учителя':
        await send_for_needed_users(data["text"], msg, settings.teacher_ids, state)
    elif data['who'] == 'Все пользователи':
        await send_for_needed_users(data["text"], msg, settings.user_ids, state)
    else:
        await state.clear()


async def send_for_needed_users(text: str, msg: types.Message, user_list, state: FSMContext):
    for user in user_list:
        await msg.bot.send_message(user, text, parse_mode=ParseMode.HTML)
        await state.clear()
