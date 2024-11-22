from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from src.Utils.database_methods import is_registered
from src.Utils.keyboards import get_contact, change_data
from src.Utils.messages import *

router = Router(name=__name__)