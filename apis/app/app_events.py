import logging
from rabbit.base import connect_rabbit


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