from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def handle_text(message: Message):
    if message.text.lower() == "привет":
        await message.answer("Привет!")
    else:
        await message.answer("Не понимаю, что это значит.")
