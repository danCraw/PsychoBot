import logging


async def start_bot(_=None) -> None:
    from db.base import database

    logging.info("connecting to postgresql")
    await database.connect()
    logging.info("Database connection - successful")


async def stop_bot(_=None) -> None:
    from db.base import database
    logging.info("Closing connection to postgresql")
    await database.disconnect()
    logging.info("Database connection - closed")