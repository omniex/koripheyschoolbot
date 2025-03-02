from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder, InlineKeyboardButton


async def get_contact() -> ReplyKeyboardMarkup:
    row = KeyboardButton(text='☎️Отправить контакт', request_contact=True)
    rows = [row]
    markup = ReplyKeyboardMarkup(
        keyboard=[rows],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


async def change_data() -> InlineKeyboardMarkup:
    accept_button = InlineKeyboardButton(
        text='✅Все правильно',
        callback_data='btn_accept'
    )

    change_button = InlineKeyboardButton(
        text='⚙️Изменить',
        callback_data='btn_change'
    )
    row = [accept_button, change_button]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


async def approve_or_reject(user_id: int) -> InlineKeyboardMarkup:
    accept_button = InlineKeyboardButton(
        text='✅Принять',
        callback_data=f'btn_approve:{user_id}'
    )

    reject_button = InlineKeyboardButton(
        text='❌Отклонить',
        callback_data=f'btn_reject:{user_id}'
    )
    row = [accept_button, reject_button]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


async def completed_or_not(ticket_id: int) -> InlineKeyboardMarkup:
    accept_button = InlineKeyboardButton(
        text='✅Заявка выполнена',
        callback_data=f'btn_completed:{ticket_id}'
    )

    in_work_button = InlineKeyboardButton(
        text='🛠️Взять в работу',
        callback_data=f'btn_in_work:{ticket_id}'
    )

    reject_button = InlineKeyboardButton(
        text='❌Заявка отклонена',
        callback_data=f'btn_not_completed:{ticket_id}'
    )
    # row = [accept_button, in_work_button, reject_button]
    rows = [[accept_button], [in_work_button], [reject_button]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


async def get_food_marks() -> ReplyKeyboardMarkup:
    button_good = KeyboardButton(
        text='✅Мне всё понравилось',
        callback_data='btn_good'
    )
    # button_not_good = KeyboardButton(
    #     text='Мне понравилось не всё'
    # )
    button_bad = KeyboardButton(
        text='❌Мне не понравилось',
        callback_data='btn_change'
    )
    row = [button_good, button_bad]
    rows = [row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)
    return markup


async def get_meal() -> ReplyKeyboardMarkup:
    btn_breakfast = KeyboardButton(
        text='Завтрак',
        callback_data='breakfast',
    )
    btn_lunch = KeyboardButton(
        text='Обед',
        callback_data='lunch',
    )
    btn_dinner = KeyboardButton(
        text='Ужин',
        callback_data='dinner',
    )
    row = [btn_breakfast, btn_lunch, btn_dinner]
    rows = [row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)
    return markup


async def get_for_who_is_announcement() -> ReplyKeyboardMarkup:
    btn_admins = KeyboardButton(
        text='🥷Администрация'
    )
    btn_council = KeyboardButton(
        text='🫂Совет Гимназистов'
    )
    btn_teachers = KeyboardButton(
        text='👸Учителя'
    )
    btn_all_users = KeyboardButton(
        text='Все пользователи'
    )
    row = [btn_admins, btn_council, btn_teachers, btn_all_users]
    rows = [row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)
    return markup


async def get_user_menu(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text="🔔 Напоминания", callback_data="btn_notes")],
        # [InlineKeyboardButton(text="🏫 Расписание", callback_data="btn_schedule")],
        [InlineKeyboardButton(text="📰 Новости", callback_data=f"btn_get_news:{user_id}")],
        # [InlineKeyboardButton(text="⬆️ Личное сообщение", callback_data="btn_direct")],
        [InlineKeyboardButton(text="📢 Создать жалобу", callback_data=f"btn_create_ticket:{user_id}")],
        [InlineKeyboardButton(text="❓ Информация", callback_data="btn_info")],
    ])


async def get_admin_menu(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔎 Найти пользователя", callback_data="btn_search_user")],
        [InlineKeyboardButton(text="📋 Список пользователей", callback_data="btn_list_users")],
        [InlineKeyboardButton(text="📣 Создать объявление", callback_data="btn_send_announcement")],
        # [InlineKeyboardButton(text="🏫 Расписание", callback_data="btn_manage_schedule")],
        [InlineKeyboardButton(text="📰 Новости", callback_data=f"btn_get_news:{user_id}"),
         InlineKeyboardButton(text="📰 Создать новость", callback_data="btn_make_news")],
        [InlineKeyboardButton(text="📢 Список жалоб", callback_data="btn_tickets_list")],
        [InlineKeyboardButton(text="🍴 Контроль питания", callback_data="btn_food")],
        # [InlineKeyboardButton(text="⚙ База данных", callback_data="btn_database_exec")],
    ])


async def search_for_users_kb(data) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for user in data:
        keyboard.add(KeyboardButton(text=f'{user[1]} {user[2]}'))
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
