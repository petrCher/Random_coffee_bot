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

    user = await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    if user:
        await message.answer(
            f"Привет, {username}!\nТы уже зарегистрирован"
        )
        return
    await Users.create(session=session, tg_id=user_id)
    await message.answer(
        f"Привет, {username}!\n{Answers.start_message}"
    )
    return
