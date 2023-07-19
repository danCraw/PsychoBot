from typing import Final
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

KB_SELECT_PSYCHOLOGIST: Final = InlineKeyboardMarkup(1)
KB_SELECT_PSYCHOLOGIST.add(
    InlineKeyboardButton("Выбрать ✅️")
)

