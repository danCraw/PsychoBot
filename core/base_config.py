import os
from typing import Optional
from dotenv import load_dotenv

from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class BaseConfig(BaseSettings):
    DESCRIPTION = "App description"
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "UTC"
    SERVICE_NAME = "AppService"
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "DEV")
    API_V1_STR: str = "/api/v1"

    # Database config
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DATABASE_URL: Optional[PostgresDsn] = os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME
    )
    DB_MIN_SIZE: int = 2
    DB_MAX_SIZE: int = 15
    DB_FORCE_ROLL_BACK: bool = False
    # Redis config
    REDIS_URL = 'redis://localhost'
    EXPIRE_TIME = 1200

    # Rabbit config
    rabbit_host: str = os.environ.get("RABBIT_HOST")
    rabbit_port: int = 5672
    rabbit_user: str = 'psycho'
    rabbit_secret: str = 'password'
    rabbit_virtual_host: str = 'psycho'
    rabbit_prefetch_count: int = 10
    rabbit_tg_events_queue_name: str = 'tg_events'
    routing_key = 'tg_events'


class DevConfig(BaseConfig):
    DESCRIPTION = "Dev web description"
    DEBUG = True


class TestConfig(BaseConfig):
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
    return FactoryConfig(BaseConfig().ENVIRONMENT)()


config = get_configuration()
