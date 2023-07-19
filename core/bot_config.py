import os
from typing import Optional

from pydantic import PostgresDsn

from core.base_config import BaseConfig


class BotConfig(BaseConfig):
    ADMINS_IDS = [677000194]

    BOT_TOKEN = '5551831184:AAF1NUw2ojoiwIWeNEFaXEkYXEGvH7sdI2g'

    YOTOKEN = '381764678:TEST:40164'

    # text const
    ADMIN_TEXT = 'Администратор\nhttps://t.me//kirili13\nНомер телефона: 8 (999) 700-91-92'


class DevConfig(BotConfig):
    DESCRIPTION = "Dev web description"
    DEBUG = True


class TestConfig(BotConfig):
    DESCRIPTION = "Dev web description"
    DEBUG = True
    TESTING = True
    DB_FORCE_ROLL_BACK = True


class FactoryConfig:
    """Returns a config instance depends on the ENV_STATE variable."""

    def __init__(self, environment: Optional[str] = "DEV"):
        self.environment = environment

    def __call__(self):
        if self.environment == "TEST":
            return TestConfig()
        return DevConfig()


def get_configuration():
    return FactoryConfig(BotConfig().ENVIRONMENT)()


config = get_configuration()
