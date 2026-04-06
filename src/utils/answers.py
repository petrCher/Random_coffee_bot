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
    help = "Я рандом кофе бот для встреч\n" "/help - вывести все команды\n" "/..."
    start_message = (
        "Я бот еженельного распределения пользователей на пары для общения!"
        "Для удобного использования у меня есть вывод команд через /help\n"
        "А пока тебе необходимо для дальнейшего использования пройти регистрацию"
    )
