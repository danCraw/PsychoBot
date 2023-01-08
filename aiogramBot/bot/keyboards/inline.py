from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

KB_SHOW_SCHEDULE: Final = InlineKeyboardMarkup(1)
KB_SHOW_SCHEDULE.add(
    InlineKeyboardButton("Узнать расписание на неделю 📆")
)

