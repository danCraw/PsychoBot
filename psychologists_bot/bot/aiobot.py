from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from core.base_config import config


def get_aiobot():
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    db = Dispatcher(bot)
    return db


bot = get_aiobot()
