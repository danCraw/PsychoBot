from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

KB_START_BOT: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
KB_START_BOT.add(KeyboardButton(text="Начать ✅"))

KB_BEGIN: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
KB_BEGIN.add(KeyboardButton(text="Выбрать 🔎"))
