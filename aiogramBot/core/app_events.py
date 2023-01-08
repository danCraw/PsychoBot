import logging
from typing import Callable


async def start_app(dp) -> None:
    from aiogramBot.db.base import database

    logging.info("connecting to a postgresql")
    await database.connect()
    logging.info("Database connection - successful")


async def stop_app(dp) -> None:
    from aiogramBot.db.base import database

    logging.info("Closing connection to postgresql")
    await database.disconnect()
    logging.info("Database connection - closed")
