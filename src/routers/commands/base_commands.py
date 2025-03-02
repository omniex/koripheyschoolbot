from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from src.Utils.database_methods import *
from src.Utils.keyboards import *
from src.Utils.messages import *
from src.config import settings

router = Router(name=__name__)


class NoteForm(StatesGroup):
    text = State()
    interval = State()


class ReportForm(StatesGroup):
    get_text = State()
    get_room = State()


@router.message(F.from_user.id.in_(settings.pending_users))
async def handle_pending(msg: types.Message):
    if msg.from_user.id in settings.admin_ids:
        await change_status(msg.from_user.id, 'approved', msg)
        await msg.answer(
            'Здравствуйте администратор, повторите сообщение, ваша заявка была одобрена автоматически, вам доступны все команды!', reply_markup=ReplyKeyboardRemove())
        return
        # settings.pending_users.discard(msg.from_user.id)
        # settings.approved_users.add(msg.from_user.id)
    await msg.answer('Пока вы не можете использовать бота, но Ваша заявка уже обрабатывается. Пожалуйста, подождите!', reply_markup=ReplyKeyboardRemove())


@router.message(F.from_user.id.in_(settings.rejected_users))
async def handle_pending(msg: types.Message):
    if msg.from_user.id in settings.admin_ids:
        await change_status(msg.from_user.id, 'approved', msg)
        await msg.answer(
            'Здравствуйте администратор, повторите сообщение, ваша заявка была одобрена автоматически, вам доступны все команды!', reply_markup=ReplyKeyboardRemove())
        return
        # settings.pending_users.discard(msg.from_user.id)
        # settings.approved_users.add(msg.from_user.id)
    await msg.answer(
        'К сожалению, Ваша заявка была отклонена администратором. Пожалуйста, подойдите лично к одному из администраторов, если это была ошибка!', reply_markup=ReplyKeyboardRemove())


@router.message(CommandStart())
async def handle_start(msg: types.Message, state: FSMContext):
    # print(get_status(msg.from_user.id))
    # print(settings.pending_users)
    await state.clear()
    registered = await is_registered(msg)
    if registered:
        await msg.answer(START_MESSAGE_REGISTERED, reply_markup=ReplyKeyboardRemove())
        await handle_menu(msg)
    else:
        await msg.answer(START_MESSAGE_NOT_REGISTERED, reply_markup=ReplyKeyboardRemove())


@router.message(Command('cancel'))
async def handel_cancel(msg: types.Message, state: FSMContext):
    await msg.answer('Действие отменено', reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command('menu'), F.from_user.id.in_(settings.user_ids))
async def handle_menu(msg: types.Message):
    await msg.answer(USERS_MENU_MESSAGE, reply_markup=await get_user_menu(msg.from_user.id), parse_mode=ParseMode.MARKDOWN)


@router.message(Command('news'))
async def handle_news(msg: types.Message, user_id: int = None):
    if user_id is None:
        user_id = msg.from_user.id
    await msg.answer('Сейчас я отправлю вам все последние новости, подождите!', reply_markup=ReplyKeyboardRemove())
    news = await get_all('news', 'NEWS')
    if len(news) == 0:
        await msg.answer(f'Новостей еще не было')
        return
    for i in news:
        # print(i)
        if i[1] == '🥷Администрация':
            if user_id in settings.admin_ids:
                await msg.answer(f'Новость от: {i[3]}\n\n{i[2]}', parse_mode=ParseMode.MARKDOWN)
        elif i[1] == '🫂Совет Гимназистов':
            if user_id in settings.council_ids or user_id in settings.admin_ids:
                await msg.answer(f'Новость от: {i[3]}\n\n{i[2]}', parse_mode=ParseMode.MARKDOWN)
        elif i[1] == '👸Учителя':
            if user_id in settings.teacher_ids or user_id in settings.admin_ids:
                await msg.answer(f'Новость от: {i[3]}\n\n{i[2]}', parse_mode=ParseMode.MARKDOWN)
        elif i[1] == 'Все пользователи':
            if user_id in settings.user_ids:
                await msg.answer(f'Новость от: {i[3]}\n\n{i[2]}', parse_mode=ParseMode.MARKDOWN)

#note define
# @router.message(Command('note'))
# async def start_note(message: types.Message, state: FSMContext):
#     await message.answer("📌 Напишите текст напоминания:")
#     await state.set_state(NoteForm.text)
#
#
# @router.message(NoteForm.text)
# async def get_note_text(message: types.Message, state: FSMContext):
#     await state.update_data(text=message.text)
#     await message.answer("⏳ Укажите интервал в минутах:")
#     await state.set_state(NoteForm.interval)
#
#
# @router.message(NoteForm.interval)
# async def save_note(message: types.Message, state: FSMContext):
#     try:
#         interval = int(message.text)
#         if interval <= 0:
#             raise ValueError
#     except ValueError:
#         await message.answer("⚠ Ошибка! Введите число больше 0.")
#         return
#
#     data = await state.get_data()
#     text = data["text"]
#
#     db = sqlite3.connect("notes.db")
#     cursor = db.cursor()
#     cursor.execute("INSERT INTO notes (user_id, note, interval, next_send) VALUES (?, ?, ?, ?)",
#                    (message.from_user.id, text, interval * 60, int(time.time()) + interval * 60))
#     db.commit()
#     db.close()
#
#     await message.answer(f"✅ Напоминание сохранено!\n📢 {text}\n🔁 Повтор каждые {interval} минут.")
#     await state.clear()


# @router.message(Command("schedule"))
# async def send_schedule(msg: types.Message):
#     user_class = "10А"
#
#     img_buf = generate_schedule_screenshot("data/schedule.xlsx", user_class)
#
#     if img_buf:
#         await msg.answer_photo(photo=img_buf, caption=f"📅 Расписание для {user_class}")
#     else:
#         await msg.answer("❌ Расписание для вашего класса не найдено.")


@router.message(Command('help'))
async def handle_help(msg: types.Message):
    if msg.from_user.id in settings.admin_ids:
        await msg.answer(HELP_COMMANDS_MESSAGE_ADMIN, reply_markup=ReplyKeyboardRemove())
        return
    if msg.from_user.id in settings.council_ids:
        await msg.answer(HELP_COMMANDS_MESSAGE_COUNCIL, reply_markup=ReplyKeyboardRemove())
        return
    await msg.answer(HELP_COMMANDS_MESSAGE_USERS, reply_markup=ReplyKeyboardRemove())


@router.message(Command('report'))
async def handle_report(msg: types.Message, state: FSMContext, user_id: int = None):
    await msg.answer('Введите текст жалобы', reply_markup=ReplyKeyboardRemove())
    if user_id is None:
        print(user_id)
        user_id = msg.from_user.id
    await state.update_data(user_id=user_id)
    await state.update_data(full_name=await get_full_name(user_id))
    await state.set_state(ReportForm.get_text)


@router.message(ReportForm.get_text)
async def handle_get_text(msg: types.Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await msg.answer('Введите номер кабинета')
    await state.set_state(ReportForm.get_room)


@router.message(ReportForm.get_room)
async def handle_get_text(msg: types.Message, state: FSMContext):
    await state.update_data(room=msg.text)
    await state.update_data(status='new')
    data = await state.get_data()
    ticket_id = await register_ticket(data)
    for user in settings.admin_ids:
        from src.main import bot
        await bot.send_message(user, f'Новая жалоба от "{data["full_name"]}"\n\n{data["text"]}\n\nКабинет: {data["room"]}', reply_markup=await completed_or_not(ticket_id=ticket_id))
    await msg.answer('Спасибо за вашу жалобу! Она будет направлена в администрацию и обработана в кратчайшие сроки.')
    await state.clear()


@router.message(Command('info'))
async def handle_start(msg: types.Message):
    await msg.answer(INFO_MESSAGE, reply_markup=ReplyKeyboardRemove())
    # settings.student_ids.add({msg.from_user.id, msg.contact.first_name, msg})

# @router.message(Command('help'), F.from_user.id.in_(settings.admin_ids))
# async def handle_start(msg: types.Message):
#     await msg.answer(HELP_COMMANDS_MESSAGE_ADMIN)
