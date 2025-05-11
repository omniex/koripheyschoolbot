import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types

from src.Utils.excel_image_schedule import get_schedule_from_excel
from src.routers import router as main_router
from src.config import settings
from src.Utils.database_methods import create_users_db, sync_db_users, create_news_db, create_notes_table, \
    create_tickets_db, sync_db_tickets, create_ideas_db

bot = Bot(settings.token)
dp = Dispatcher()


async def start():
    dp.include_router(main_router)
    await create_users_db()
    await create_news_db()
    await create_notes_table()
    await create_tickets_db()
    await create_ideas_db()
    await sync_db_users()
    await sync_db_tickets()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        #stream=sys.stdout,
        handlers=[
            logging.FileHandler("bot_logs.log", encoding="utf-8"),  # Запись в файл
            logging.StreamHandler()  # Вывод в консоль
        ]
    )
    asyncio.run(start())
