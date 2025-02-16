import asyncio
import logging
import sqlite3
import sys

from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import BotCommand

from src.routers import router as main_router
from src.config import settings
from src.Utils.database_methods import create_db
import os

bot = Bot(settings.token)
dp = Dispatcher()


async def start():
    dp.include_router(main_router)
    create_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
