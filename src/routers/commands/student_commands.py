from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.Utils.database_methods import *
from src.Utils.keyboards import *
from src.Utils.messages import *

router = Router(name=__name__)


@router.message(Command('direct'))
async def handle_direct(msg: types.Message):
    await msg.answer('Введите имя человека, которому хотите отправить сообщение'
                     'Вам будет показан данный пользователь'
                     'Нажмите на галочку, если это тот, кому вы хотите отправить сообщение')
