from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Получить список пользователей", callback_data="admin:get_users"
            )
        ],
    ]
)


@dataclass
class Answers:
    menu_admin = f"Расширенное меню команд для админов\n/admin - получение админских команд\n/menu - вывод меню\n/card - получить свою карточку"
    menu = f"Меню команд\n/menu - вывод меню\n/card - получить свою карточку"
