import logging
from db.base import connect_rabbit


async def start_app(_=None) -> None:
    from db.base import database

    logging.info("connecting to postgresql")
    await database.connect()
    logging.info("Database connection - successful")
    logging.info("connecting to rabbit")
    await connect_rabbit()
    logging.info("Rabbit connection - successful")


async def stop_app(_=None) -> None:
    from db.base import database

    logging.info("Closing connection to postgresql")
    await database.disconnect()
    logging.info("Database connection - closed")


# async def start_rabbit() -> None:
#     rabbit_conn = await aio_pika.connect_robust("amqp://{user}:{password}@{host}:{port}/{vhost}".format(
#         user=config.rabbit_user,
#         password=config.rabbit_secret,
#         host=config.rabbit_host,
#         port=config.rabbit_port,
#         vhost=config.rabbit_virtual_host
#     ))
#     rabbit_channel = await rabbit_conn.channel()
#     await rabbit_channel.set_qos(
#         prefetch_count=config.rabbit_prefetch_count  # MAX messages to process at the same time
#     )
#     await rabbit_channel.declare_queue(config.rabbit_tg_events_queue_name, auto_delete=False)
#
#
# async def stop_rabbit() -> None:
#     from db.base import rabbit_conn
#
#     await rabbit_conn.close()
