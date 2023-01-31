import os
from typing import Optional

from pydantic import BaseSettings, PostgresDsn


class GlobalConfig(BaseSettings):
    DESCRIPTION = "App description"
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "UTC"
    SERVICE_NAME = "AppService"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "DEV")
    API_V1_STR: str = "/api/v1"

    BOT_TOKEN = '5551831184:AAF1NUw2ojoiwIWeNEFaXEkYXEGvH7sdI2g'

    YOTOKEN = '381764678:TEST:40164'

    # Database config
    DATABASE_URL: Optional[PostgresDsn] = os.environ.get(
        "DATABASE_URL", "postgresql://postgresql:postgresql@0.0.0.0:5432/config"
    )
    DB_MIN_SIZE: int = 2
    DB_MAX_SIZE: int = 15
    DB_FORCE_ROLL_BACK: bool = False
    # Redis config
    REDIS_URL = 'redis://localhost'
    EXPIRE_TIME = 1200
    # text const

    ADMIN_TEXT = 'Администратор\nhttps://t.me//kirili13\nНомер телефона: 8 (999) 700-91-92'


class DevConfig(GlobalConfig):
    DESCRIPTION = "Dev web description"
    DEBUG = True


class TestConfig(GlobalConfig):
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
    return FactoryConfig(GlobalConfig().ENVIRONMENT)()


config = get_configuration()
