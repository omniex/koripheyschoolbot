from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.Utils.database_methods import *
from src.Utils.keyboards import *
from src.Utils.messages import *
from src.config import settings

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
    await state.clear()
    registered = is_registered(msg)
    if registered:
        await msg.answer(START_MESSAGE_REGISTERED)
    else:
        await msg.answer(START_MESSAGE_NOT_REGISTERED)


@router.message(Command('cancel'))
async def handel_cancel(msg: types.Message, state: FSMContext):
    await msg.answer('Действие отменено')
    await state.clear()


@router.message(Command('register'))
async def handle_registration(msg: types.Message, state: FSMContext):
    await msg.answer('Давайте начнём регистрацию!')
    await state.set_state(User.name)
    await msg.answer('Введи ваше имя')


@router.message(User.name, F.text.regexp(r'^[А-Яа-яё]{2,20}$'))
async def register_name(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text.lower().capitalize())
    await state.set_state(User.surname)
    await msg.answer('Введите вашу фамилию')


@router.message(User.surname, F.text.regexp(r'^[А-Яа-яё]{4,20}$'))
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
    user_role = get_role(msg.contact.user_id)
    await state.update_data(role=user_role)
    data = await state.get_data()
    await msg.answer(f'''
    Имя: {data["name"]}
Фамилия: {data["surname"]}
Класс: {data["grade"]}
Номер телефона: {data["phone_number"]}
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


@router.message(Command('info'))
async def handle_start(msg: types.Message):
    await msg.answer(INFO_MESSAGE)
    # settings.student_ids.add({msg.from_user.id, msg.contact.first_name, msg})


# @router.message(Command('help'), F.from_user.id.in_(settings.admin_ids))
# async def handle_start(msg: types.Message):
#     await msg.answer(HELP_COMMANDS_MESSAGE_ADMIN)