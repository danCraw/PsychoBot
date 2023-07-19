import types

import aio_pika

from core.base_config import config


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