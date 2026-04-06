from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import Users
from src.settings import get_settings
from src.utils.answers import Answers, admin_panel_kb

settings = get_settings()

router = Router()
answer = Answers()


class AdminFSM(StatesGroup):
    waiting_something = State()


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


@router.callback_query(F.data == "admin:get_users")
async def cb_addteam(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    users = await Users.query(session=session).all()
    text = "\n".join([f"ФИО: {user.name} - tg_id: {user.tg_id}" for user in users])
    await callback.message.answer(f"Список пользователей:\n{text}")
