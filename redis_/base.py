import aioredis

from core.base_config import config


def get_redis() -> aioredis.Redis:
    redis_url = config.REDIS_URL
    return aioredis.Redis(decode_responses=True)


redis_conn = get_redis()
