from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import Username, Users
from src.utils.answers import Answers

router = Router()
answer = Answers()


class RegFSM(StatesGroup):
    waiting_full_name = State()
    waiting_birthday = State()
    waiting_info = State()
    waiting_review = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not message.from_user:
        return
    user_id = message.from_user.id
    username = message.from_user.username

    user = (
        await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    )
    if user:
        await message.answer(f"Привет, {username}!\nТы уже зарегистрирован")
        return
    user = await Users.create(session=session, tg_id=user_id)
    await Username.create(session=session, id=user.id, username=username)
    await state.set_state(RegFSM.waiting_full_name)
    await message.answer(f"Привет, {username}!")
    await message.answer("Введите свое ФИО для регистрации")
    return


@router.message(RegFSM.waiting_full_name)
async def get_full_name(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    is_edit = data.get("edit_field") == "name"
    if not message.text or not message.from_user:
        await message.answer("Пожалуйста, введите корректное ФИО")
        return
    full_name = message.text
    user_id = message.from_user.id
    user = (
        await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    )
    id = user.id
    await Users.update(id=id, session=session, name=full_name)
    if is_edit:
        await message.answer("ФИО успешно обновлено!")
        await state.clear()
        await show_all_info(id, message, session)
    else:
        await state.set_state(RegFSM.waiting_birthday)
        await message.answer("Введите свою дату рождения в формате dd.mm.yyyy")


@router.message(RegFSM.waiting_birthday)
async def get_birthday(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    is_edit = data.get("edit_field") == "birthday"
    if not message.text or not message.from_user:
        await message.answer("Пожалуйста, введите дату рождения")
        return
    birthday = message.text
    user_id = message.from_user.id
    user = (
        await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    )
    id = user.id
    await Users.update(id=id, session=session, birthday=birthday)
    if is_edit:
        await message.answer("День рождения успешно обновлен!")
        await state.clear()
        await show_all_info(id, message, session)
    else:
        await state.set_state(RegFSM.waiting_info)
        await message.answer("Введите информацию о себе")


@router.message(RegFSM.waiting_info)
async def get_info(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    is_edit = data.get("edit_field") == "about"
    if not message.text or not message.from_user:
        await message.answer("Пожалуйста, введите информацию о себе")
        return
    info = message.text
    user_id = message.from_user.id
    user = (
        await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    )
    id = user.id
    await Users.update(id=id, session=session, about=info)
    if is_edit:
        await message.answer("Информация о себе успешно обновлена!")
    await state.clear()
    await show_all_info(id, message, session)


@router.message(Command("card"))
async def cmd_menu(message: Message, session: AsyncSession) -> None:
    user_id = message.from_user.id
    user = (
        await Users.query(session=session).filter(Users.tg_id == user_id).one_or_none()
    )
    id = user.id
    await show_all_info(id, message, session)


async def show_all_info(id: int, message: Message, session: AsyncSession):
    user = await Users.get(id=id, session=session)
    text = f"Твоя карточка:\nФИО - <b>{user.name}</b>\nДата рождения - <b>{user.birthday}</b>\nИнформация о себе - <b>{user.about}</b>"
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить ФИО", callback_data="edit:name")
    builder.button(text="Изменить ДР", callback_data="edit:birthday")
    builder.button(text="Изменить Инфо о себе", callback_data="edit:about")
    builder.button(text="Всё верно, оставлю", callback_data="edit:done")
    builder.adjust(1)
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(F.data.startswith("edit"))
async def edit_profile(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    action = callback.data.split(":")[1]
    if action == "done":
        await callback.message.edit_text("Отлично! Данные сохранены.")
        await state.clear()
        await callback.answer()
        return
    await state.update_data(edit_field=action)
    if action == "name":
        await callback.message.edit_text("Введите новое ФИО:")
        await state.set_state(RegFSM.waiting_full_name)
    elif action == "birthday":
        await callback.message.edit_text("Введите новую дату рождения dd.mm.yyyy:")
        await state.set_state(RegFSM.waiting_birthday)
    elif action == "about":
        await callback.message.edit_text("Введите новую информацию о себе:")
        await state.set_state(RegFSM.waiting_info)
    await callback.answer()
