from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.settings import Settings
from src.handlers import setup_routers
from src.middleware.db import DbSessionMiddleware

settings = Settings()
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)

dp = Dispatcher(storage=MemoryStorage())
dp.update.middleware(DbSessionMiddleware())
dp.include_router(setup_routers())