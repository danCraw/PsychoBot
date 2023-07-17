import types

import databases
from sqlalchemy.ext.declarative import declarative_base
import aioredis
import aio_pika

from core.config import config


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


async def connect_rabbit():
    rabbit.connection = await aio_pika.connect_robust("amqp://{user}:{password}@{host}:{port}/{vhost}".format(
        user=config.rabbit_user,
        password=config.rabbit_secret,
        host=config.rabbit_host,
        port=config.rabbit_port,
        vhost=config.rabbit_virtual_host
    ))

    channel = await rabbit.connection.channel()
    await channel.set_qos(
        prefetch_count=config.rabbit_prefetch_count  # MAX messages to process at the same time
    )
    queue = await channel.declare_queue(config.rabbit_tg_events_queue_name, auto_delete=False)

    rabbit.channel = await rabbit.connection.channel()
    rabbit.queue = queue


rabbit = types.SimpleNamespace(channel=None, queue=None, connection=None)
redis_conn = get_redis()
database = get_db()
Base = declarative_base()
metadata = Base.metadata
