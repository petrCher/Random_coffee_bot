from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.settings import get_settings
from src.utils.answers import Answers, admin_panel_kb

settings = get_settings()

router = Router()
answer = Answers()


def _is_admin(user_id: int) -> bool:
    return settings.is_admin(user_id)


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await message.answer("К сожалению, ты не являешься админом")
        return
    await message.answer(
        "<b>Админка</b>\n\nВыбери действие:",
        parse_mode="HTML",
        reply_markup=admin_panel_kb,
    )
