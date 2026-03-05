from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.utils.answers import Answers

router = Router()
answer = Answers()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n{answer.start_message}"
    )
