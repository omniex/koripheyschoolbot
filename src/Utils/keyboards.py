from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder, InlineKeyboardButton


def get_contact() -> ReplyKeyboardMarkup:
    row = KeyboardButton(text='☎️Отправить контакт', request_contact=True)
    rows = [row]
    markup = ReplyKeyboardMarkup(
        keyboard=[rows],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup


def change_data() -> InlineKeyboardMarkup:
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


def get_food_marks() -> ReplyKeyboardMarkup:
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


def get_meal() -> ReplyKeyboardMarkup:
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


def get_for_who_is_annoucement() -> ReplyKeyboardMarkup:
    btn_admins = KeyboardButton(
        text = '🥷Администрация'
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
