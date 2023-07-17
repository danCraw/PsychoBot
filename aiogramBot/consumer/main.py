import asyncio
import logging
import os
import sys

import aio_pika
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from db.base import rabbit, connect_rabbit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from core.config import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


async def main(loop):
    await connect_rabbit()
    await rabbit.queue.consume(callback_on_message)
    return rabbit.connection


async def callback_on_message(msg: aio_pika.IncomingMessage):
    print(f'[x] Received {msg.body.decode()}')
    print('[x] Done')
    await msg.ack()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    connection = loop.run_until_complete(main(loop))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
