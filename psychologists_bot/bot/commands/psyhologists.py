from aiogram import Dispatcher, types

dp = Dispatcher()


@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")
