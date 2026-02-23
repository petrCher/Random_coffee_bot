import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.settings import Settings
from src.handlers import start, help, text

settings = Settings()
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(help.router)
dp.include_router(text.router)

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    dp.run_polling(bot)