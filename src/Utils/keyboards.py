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
