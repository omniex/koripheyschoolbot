from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.Utils.database_methods import register_user, get_all
from src.config import settings
from src.routers.commands.base_commands import User

router = Router(name=__name__)


@router.callback_query(F.data == 'btn_change')
async def handle_change_info_kb(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(User.name)
    await callback_query.message.answer('Введите своё имя')


@router.callback_query(F.data == 'btn_accept')
async def handle_change_info_kb(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = await state.get_data()
    users_list = get_all('users', 'USERS')
    iss = False
    if users_list:
        for user in users_list:
            print(callback_query.from_user.id, callback_query.message.from_user.id, callback_query.id)
            if callback_query.from_user.id == user[7]:
                iss = True
        if iss:
            await callback_query.message.answer('Вы уже зарегистрированы')
        else:
            settings.user_ids.add(callback_query.from_user.id)
            register_user(data)
            await callback_query.message.answer('Спасибо, что зарегистрировались!\nВаша заявка отправлена '
                                                'администратору и после проверки, вы получите уведомление и сможете '
                                                'начать пользоваться возможностями бота')
    else:
        settings.user_ids.add(callback_query.from_user.id)
        register_user(data)
        await callback_query.message.answer('Спасибо, что зарегистрировались!\nВаша заявка отправлена '
                                                'администратору и после проверки, вы получите уведомление и сможете '
                                                'начать пользоваться возможностями бота')
    await state.clear()
