from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.utils.answers import Answers
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db import Users
from sqlalchemy import select

router = Router()
answer = Answers()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession)-> None:
    if not message.from_user:
        return
    user_id=message.from_user.id
    username=message.from_user.username

    existing = await session.execute(
        select(Users).where(Users.tg_id==user_id)
    )
    user=existing.scalar_one_or_none()
    if user:
        await message.answer(
            f"Привет, {username}!\nТы уже зарегистрирован"
        )
        return
    await message.answer(
        f"Привет, {username}!\n{Answers.start_message}"
    )
    return
