from aiogram import Router
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State

from src.Utils.database_methods import register_user, get_all_users
from src.Utils.keyboards import get_contact, change_data
from src.Utils.messages import START_MESSAGE, HELP_MESSAGE
from src.config import settings
from src.Utils import keyboards

router = Router(name=__name__)


class User(StatesGroup):
    name = State()
    surname = State()
    grade = State()
    name_in_tg = State()
    id = State()
    phone_number = State()
    username = State()
    change = State()


@router.message(CommandStart())
async def handle_start(msg: types.Message, state: FSMContext):
    await msg.answer(START_MESSAGE)
    users_list = get_all_users()
    iss = False
    if users_list:
        for user in users_list:
            if msg.from_user.id == user[7]:
                iss = True
                await msg.answer(f'Здравствуйте {user[1]}!')
                break
        if not iss:
            await msg.answer('Вы не зарегистрированы, давайте зарегистрируемся!')
            await state.set_state(User.name)
            await msg.answer('Введите своё имя')
    else:
        await msg.answer('Вы не зарегистрированы, давайте зарегистрируемся!')
        await state.set_state(User.name)
        await msg.answer('Введите своё имя')


@router.message(Command('cancel'))
async def handel_cancel(msg: types.Message, state: FSMContext):
    await msg.answer('Действие отменено')
    await state.clear()


@router.message(User.name, F.text.regexp(r'^[А-Яа-я]{2,20}$'))
async def register_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text.lower().capitalize())
    await state.set_state(User.surname)
    await msg.answer('Введите вашу фамилию')


@router.message(User.surname, F.text.regexp(r'^[А-Яа-я]{4,20}$'))
async def register_surname(msg: types.Message, state: FSMContext):
    await state.update_data(surname=msg.text.lower().capitalize())
    await state.set_state(User.grade)
    await msg.answer('Введите ваш класс (вместе с буквой)')


@router.message(User.grade, F.text.regexp(r'^([1])?(?(1)[01]|[0123456789])[А-Яа-я]$'))
async def register_phone(msg: types.Message, state: FSMContext):
    await state.update_data(grade=msg.text.upper())
    await state.set_state(User.phone_number)
    await msg.answer('Поделитесь вашим контактом для завершения регистрации', reply_markup=get_contact(), one_time_keyboard=True)


@router.message(F.contact, User.phone_number)
async def handle_contact(msg: types.Message, state: FSMContext):
    await state.update_data(phone_number=msg.contact.phone_number)
    await state.update_data(username=msg.from_user.username)
    await state.update_data(id=msg.contact.user_id)
    await state.update_data(name_in_tg=msg.contact.first_name)
    data = await state.get_data()
    await msg.answer(f'''
    Имя: {data["name"]}
Фамилия: {data["surname"]}
Класс: {data["grade"]}
Номер телефона: {data["phone_number"]}
Имя в телеграм: {data["name_in_tg"]}
username: {data["username"]}
user_id: {data["id"]}
    ''', reply_markup=change_data())


@router.message(User.name)
async def handle_incorrect(msg: types.Message):
    await msg.answer('❌Вы ввели неправильное имя, попробуйте еще раз,'
                     ' для имени разрешены только символы русского алфавита, при каких либо вопросах,'
                     ' обратитесь к администрации')


@router.message(User.surname)
async def handle_incorrect(msg: types.Message):
    await msg.answer('❌Вы ввели неправильную фамилию, попробуйте еще раз,'
                     ' для фамиилии разрешены только символы русского алфавита, при каких либо вопросах,'
                     ' обратитесь к администрации')


@router.message(User.grade)
async def handle_incorrect(msg: types.Message):
    await msg.answer('❌Вы ввели неправильный класс, попробуйте еще раз,'
                     ' при каких либо вопросах,'
                     ' обратитесь к администрации')


@router.message(Command('help'))
async def handle_start(msg: types.Message):
    await msg.answer(HELP_MESSAGE)
    # settings.student_ids.add({msg.from_user.id, msg.contact.first_name, msg})
