import databases
from sqlalchemy.ext.declarative import declarative_base
import aioredis

from aiogramBot.core.config import config


def get_db() -> databases.Database:
    database_url = config.DATABASE_URL
    options = {
        "min_size": config.DB_MIN_SIZE,
        "max_size": config.DB_MAX_SIZE,
        "force_rollback": config.DB_FORCE_ROLL_BACK,
    }

    return databases.Database(database_url, **options)


def get_redis() -> aioredis.Redis:
    redis_url = config.REDIS_URL
    return aioredis.Redis(decode_responses=True)


redis_conn = get_redis()
database = get_db()
Base = declarative_base()
metadata = Base.metadata
