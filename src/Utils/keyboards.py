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
    button_not_good = KeyboardButton(
        text='Мне понравилось не всё'
    )
    button_bad = KeyboardButton(
        text='❌Мне не понравилось',
        callback_data='btn_change'
    )
    row = [button_good, button_bad]
    rows = [row]
    markup = ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)
    return markup