import asyncio

from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from src.Utils.database_methods import *
from src.Utils.keyboards import *
from src.config import settings
from aiogram.fsm.state import StatesGroup, State

from src.routers.commands.admin_commands import send_for_needed_users

router = Router(name=__name__)


class Announcement(StatesGroup):
    for_who_teacher = State()
    wait_text_teacher = State()


@router.message(Command('announcement'), F.from_user.id.in_(settings.teacher_ids))
async def handle_admin_announcement(msg: types.Message, state: FSMContext):
    await msg.answer('Напишите, какой класс должен увидеть это оповещение (в формате "10А")',)
    await state.set_state(Announcement.for_who_teacher)


@router.message(Announcement.for_who_teacher)
async def handle_what_announcement(msg: types.Message, state: FSMContext):
    await state.update_data(who=msg.text)
    data = await state.get_data()
    all_the_classes = ['1А', '1Б', '1В', '1Г', '1Д', '1Е', '1Ё', '1Ж', '1З', '1И', '1Й', '1К', '1Л', '1М', '1Н', '1О',
                       '1П', '1Р', '1С', '1Т', '1У', '1Ф', '1Х', '1Ц', '1Ч', '1Ш', '1Щ', '1Ы', '1Э', '1Ю', '1Я', '2А',
                       '2Б', '2В', '2Г', '2Д', '2Е', '2Ё', '2Ж', '2З', '2И', '2Й', '2К', '2Л', '2М', '2Н', '2О', '2П',
                       '2Р', '2С', '2Т', '2У', '2Ф', '2Х', '2Ц', '2Ч', '2Ш', '2Щ', '2Ы', '2Э', '2Ю', '2Я', '3А', '3Б',
                       '3В', '3Г', '3Д', '3Е', '3Ё', '3Ж', '3З', '3И', '3Й', '3К', '3Л', '3М', '3Н', '3О', '3П', '3Р',
                       '3С', '3Т', '3У', '3Ф', '3Х', '3Ц', '3Ч', '3Ш', '3Щ', '3Ы', '3Э', '3Ю', '3Я', '4А', '4Б', '4В',
                       '4Г', '4Д', '4Е', '4Ё', '4Ж', '4З', '4И', '4Й', '4К', '4Л', '4М', '4Н', '4О', '4П', '4Р', '4С',
                       '4Т', '4У', '4Ф', '4Х', '4Ц', '4Ч', '4Ш', '4Щ', '4Ы', '4Э', '4Ю', '4Я', '5А', '5Б', '5В', '5Г',
                       '5Д', '5Е', '5Ё', '5Ж', '5З', '5И', '5Й', '5К', '5Л', '5М', '5Н', '5О', '5П', '5Р', '5С', '5Т',
                       '5У', '5Ф', '5Х', '5Ц', '5Ч', '5Ш', '5Щ', '5Ы', '5Э', '5Ю', '5Я', '6А', '6Б', '6В', '6Г', '6Д',
                       '6Е', '6Ё', '6Ж', '6З', '6И', '6Й', '6К', '6Л', '6М', '6Н', '6О', '6П', '6Р', '6С', '6Т', '6У',
                       '6Ф', '6Х', '6Ц', '6Ч', '6Ш', '6Щ', '6Ы', '6Э', '6Ю', '6Я', '7А', '7Б', '7В', '7Г', '7Д', '7Е',
                       '7Ё', '7Ж', '7З', '7И', '7Й', '7К', '7Л', '7М', '7Н', '7О', '7П', '7Р', '7С', '7Т', '7У', '7Ф',
                       '7Х', '7Ц', '7Ч', '7Ш', '7Щ', '7Ы', '7Э', '7Ю', '7Я', '8А', '8Б', '8В', '8Г', '8Д', '8Е', '8Ё',
                       '8Ж', '8З', '8И', '8Й', '8К', '8Л', '8М', '8Н', '8О', '8П', '8Р', '8С', '8Т', '8У', '8Ф', '8Х',
                       '8Ц', '8Ч', '8Ш', '8Щ', '8Ы', '8Э', '8Ю', '8Я', '9А', '9Б', '9В', '9Г', '9Д', '9Е', '9Ё', '9Ж',
                       '9З', '9И', '9Й', '9К', '9Л', '9М', '9Н', '9О', '9П', '9Р', '9С', '9Т', '9У', '9Ф', '9Х', '9Ц',
                       '9Ч', '9Ш', '9Щ', '9Ы', '9Э', '9Ю', '9Я', '10А', '10Б', '10В', '10Г', '10Д', '10Е', '10Ё', '10Ж',
                       '10З', '10И', '10Й', '10К', '10Л', '10М', '10Н', '10О', '10П', '10Р', '10С', '10Т', '10У', '10Ф',
                       '10Х', '10Ц', '10Ч', '10Ш', '10Щ', '10Ы', '10Э', '10Ю', '10Я', '11А', '11Б', '11В', '11Г', '11Д',
                       '11Е', '11Ё', '11Ж', '11З', '11И', '11Й', '11К', '11Л', '11М', '11Н', '11О', '11П', '11Р', '11С',
                       '11Т', '11У', '11Ф', '11Х', '11Ц', '11Ч', '11Ш', '11Щ', '11Ы', '11Э', '11Ю', '11Я']
    if str(data['who']).upper() in all_the_classes:
        await msg.answer(
            f'Хорошо, только "{data["who"]}" увидит(-ят) эту информацию. Теперь введите текст самого оповещения', reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer(
            f'Класс "{data["who"]}" не существует. Пожалуйста, введите корректное название класса в формате НОМЕРБУКВА', reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(Announcement.wait_text_teacher)


@router.message(Announcement.wait_text_teacher)
async def handle_announcement_text(msg: types.Message, state: FSMContext):
    await state.update_data(text=msg.text)
    data = await state.get_data()
    for user in await get_all('users', 'USERS'):
        if user[3] == data['who']:
            try:
                await msg.copy_to(chat_id=user[7],
                                  reply_markup=ReplyKeyboardRemove())  # Копирует ВСЁ сообщение (текст, фото, видео и т. д.)
            except Exception as e:
                await msg.answer(f"Ошибка при отправке пользователю {user}: {e}", reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(0.1)
    await msg.answer('Оповещение успешно отправлено всем пользователям')
    await state.clear()