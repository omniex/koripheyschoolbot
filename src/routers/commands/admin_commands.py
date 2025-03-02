import asyncio
import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, ReplyKeyboardRemove

from src.Utils.database_methods import *
from src.Utils.messages import ADMIN_MENU_MESSAGE
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


class SearchUser(StatesGroup):
    search_name = State()


@router.message(Command('admin'), F.from_user.id.in_(settings.user_ids))
async def handle_menu(msg: types.Message):
    await msg.answer(ADMIN_MENU_MESSAGE, parse_mode=ParseMode.MARKDOWN,
                     reply_markup=await get_admin_menu(msg.from_user.id))


@router.message(Command('users'), F.from_user.id.in_(settings.admin_ids))
async def handle_user_list(msg: types.Message):
    await msg.reply('Hello admin')
    await msg.answer('Here is the list of all users: ')
    all_users = await get_all('users', 'USERS')
    users_info = ''
    for user in all_users:
        users_info += f'UID: {user[0]}\nName: {user[1]}\nSurname: {user[2]}\nGrade: {user[3]}\nPhone number: {user[4]}\nTelegram name: {user[5]}\nUsername: @{user[6]}\nId: {user[7]}\nRole: {user[8]}\n\n'
    if users_info == '':
        await msg.answer('Nothing in database', reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(users_info, reply_markup=ReplyKeyboardRemove())


@router.message(Command('database_exec'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    args = msg.text.split()
    if len(args) < 3:
        await msg.answer('Command using: /database_exec <database name> <command>', reply_markup=ReplyKeyboardRemove())
        return
    ind = len(f'{args[0]} {args[1]}')
    await msg.answer(f'Trying to execute command: {msg.text[ind:]}', reply_markup=ReplyKeyboardRemove())
    try:
        await execute_command(msg.text[ind:], args[1])
    except Exception as e:
        await msg.answer(str(e))


@router.message(Command('database_get'), F.from_user.id.in_(settings.admin_ids))
async def handle_database(msg: types.Message):
    args = msg.text.split()
    if len(args) < 3:
        await msg.answer('Command using: /database_get <database name> <command>', reply_markup=ReplyKeyboardRemove())
        return
    ind = len(f'{args[0]} {args[1]}')
    await msg.answer(f'Trying to execute command: {msg.text[ind:]}', reply_markup=ReplyKeyboardRemove())
    try:
        data = await get_command(msg.text[ind:], args[1])
        await msg.answer(f'Raw data: \n{data}')
    except Exception as e:
        await msg.answer(str(e))


@router.message(Command('search'), F.from_user.id.in_(settings.admin_ids))
async def search_user(msg: types.Message, state: FSMContext):
    # args = msg.text.split()
    # if len(args) > 1:
    #     await msg.answer('Command using: /search')
    #     return
    await msg.answer('Введите имя/фамилию пользователя', reply_markup=ReplyKeyboardRemove())
    await state.set_state(SearchUser.search_name)


@router.message(SearchUser.search_name)
async def search_for_user(msg: types.Message, state: FSMContext):
    name = msg.text
    data = await search_for_direct_data('users', 'USERS', name)
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
    await create_db_food()
    arr = msg.text.split()

    if len(arr) < 2 or not arr[1].isdigit():
        await msg.answer("Использование: /food <количество>", reply_markup=ReplyKeyboardRemove())
        return

    FoodSurvey.need = int(arr[1])
    FoodSurvey.msg_con = msg
    FoodSurvey.state_con = state

    await msg.answer("Какой это приём пищи?", reply_markup=await get_meal())
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
            f'Приём пищи: {meal}\nВсего ответов: {good + bad}\nПроцент понравившихся: {good / (good + bad) * 100}%\n✅ Понравилось: {good}\n❌ Не понравилось: {bad}', reply_markup=ReplyKeyboardRemove())
        await register_meal(data)
        await state.clear()
        return

    await msg.answer(f'Обрабатываю ответ - {remaining}', reply_markup=await get_food_marks())
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
        await msg.answer('Command using: /export_excel <database name> <table name>', reply_markup=ReplyKeyboardRemove())
        return
    try:
        await export_to_excel(args[1], args[2])
        await msg.answer_document(FSInputFile(f'{args[2]}.xlsx'))
        os.remove(f'{args[2]}.xlsx')
    except Exception as e:
        print(e)


@router.message(Command('change_role'), F.from_user.id.in_(settings.admin_ids))
async def handle_changing_role(msg: types.Message):
    args = msg.text.split()
    if len(args) != 3:
        await msg.answer('Command using: /change_role <user_id> <new_role>', reply_markup=ReplyKeyboardRemove())
        return

    if args[2] == 'admin':
        await msg.answer('Nobody can give admin role, you need to add it manually in code', reply_markup=ReplyKeyboardRemove())

    try:
        await change_role(int(args[1]), args[2], msg)
    except Exception as e:
        print(e)


@router.message(Command('change_status'), F.from_user.id.in_(settings.admin_ids))
async def handle_changing_role(msg: types.Message):
    args = msg.text.split()
    if len(args) != 3:
        await msg.answer('Command using: /change_status <user_id> <new_status (approved, rejected, pending)>', reply_markup=ReplyKeyboardRemove())
        return

    try:
        await change_status(int(args[1]), args[2], msg)
    except Exception as e:
        print(e)


@router.message(Command('announcement'), F.from_user.id.in_(settings.admin_ids))
async def handle_admin_announcement(msg: types.Message, state: FSMContext):
    await msg.answer('Выберите, кто должен увидеть это оповещение', reply_markup=await get_for_who_is_announcement())
    await state.set_state(Announcement.for_who)


@router.message(Announcement.for_who)
async def handle_what_announcement(msg: types.Message, state: FSMContext):
    await state.update_data(who=msg.text)
    data = await state.get_data()
    await msg.answer(
        f'Хорошо, только "{data["who"]}" увидит(-ят) эту информацию. Теперь введите текст самого оповещения', reply_markup=ReplyKeyboardRemove())
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


async def send_for_needed_users(msg: types.Message, user_list, state: FSMContext):
    for user in user_list:
        try:
            await msg.copy_to(chat_id=user, reply_markup=ReplyKeyboardRemove())  # Копирует ВСЁ сообщение (текст, фото, видео и т. д.)
        except Exception as e:
            await msg.answer(f"Ошибка при отправке пользователю {user}: {e}", reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(0.1)  # Небольшая задержка, чтобы избежать лимитов Telegram

    await msg.answer('Оповещение успешно отправлено всем пользователям')
    await state.clear()


@router.message(Command('approve'), F.from_user.id.in_(settings.admin_ids))
async def handle_approve(msg: types.Message, state: FSMContext):
    args = msg.split()
    if len(args) != 2 or not args[1].isdigit():
        await msg.answer('Command using: /approve <user_id>', reply_markup=ReplyKeyboardRemove())
        return
    await change_status(int(args[1]), 'approved', msg)


@router.message(Command('reject'), F.from_user.id.in_(settings.admin_ids))
async def handle_reject(msg: types.Message, state: FSMContext):
    args = msg.split()
    if len(args) != 2 or not args[1].isdigit():
        await msg.answer('Command using: /reject <user_id>', reply_markup=ReplyKeyboardRemove())
        return
    await change_status(int(args[1]), 'rejected', msg)


@router.message(Command('change_ticket_status'), F.from_user.id.in_(settings.admin_ids))
async def handle_approve(msg: types.Message, state: FSMContext):
    args = msg.split()
    if len(args) != 3 or not args[1].isdigit():
        await msg.answer('Command using: /change_ticket_status <ticket_id ({user_id}_{ticket_num})> <status (new, in work, completed, not_completed)>', reply_markup=ReplyKeyboardRemove())
        return
    if args[2] == 'not_completed':
        await change_status_ticket(args[1], 'not completed', msg)
    else:
        await change_status_ticket(args[1], args[2], msg)


@router.message(Command('reports'), F.from_user.id.in_(settings.admin_ids))
async def handle_reports(msg: types.Message):
    data = await get_all('tickets', 'TICKETS')
    await msg.answer(f'Вот, что мне удалось найти:', reply_markup=ReplyKeyboardRemove())
    for ticket in data:
        if ticket[6] == 'not completed' or ticket[6] == 'in work':
            ticket_info = ''
            ticket_info += f'UID: {ticket[0]}\nticket_id: {ticket[1]}\nИмя: {ticket[2]}\nTG ID: {ticket[3]}\nИнформация: {ticket[4]}\nКабинет: {ticket[5]}\nСтатус: {ticket[6]}\n'
            await msg.answer(ticket_info, reply_markup=await completed_or_not(ticket_id=ticket[1]))
