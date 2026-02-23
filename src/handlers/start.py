from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Я бот. Приятно познакомиться, {message.from_user.first_name}!")