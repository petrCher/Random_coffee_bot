from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.settings import get_settings
from src.utils.answers import Answers

settings = get_settings()

router = Router()
answer = Answers()


def _is_admin(user_id: int) -> bool:
    return settings.is_admin(user_id)


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await message.answer(answer.menu)
    else:
        await message.answer(answer.menu_admin)
