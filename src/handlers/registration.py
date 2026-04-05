from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.utils.answers import Answers
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db import Users
from sqlalchemy import select

router = Router()
answer = Answers()

class RegFSM(StatesGroup):
    waiting_full_name = State()

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
    await state.set_state(RegFSM.waiting_full_name)
    await message.answer(
        f"Привет, {username}!\nВведи свое ФИО для регистрации"
    )
    return

@router.message(RegFSM.waiting_full_name)
async def process_full_name(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text or not message.from_user:
        await message.answer("Пожалуйста, введите корректное ФИО")
        return
    full_name=message.text
    user_id=message.from_user.id
    user = await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    id=user.id
    await Users.update(id=id, session=session, name=full_name)
    await message.answer(
        f"Твое ФИО: <b>{full_name}</b>", parse_mode="HTML"
    )