import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from src.routers import router as main_router
from src.config import settings
from src.Utils.database_methods import create_users_db, sync_db_users

bot = Bot(settings.token)
dp = Dispatcher()


async def start():
    dp.include_router(main_router)
    create_users_db()
    sync_db_users()
    print(settings.user_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
