from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.utils.answers import Answers

router = Router()
answers = Answers()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(answers.help)
