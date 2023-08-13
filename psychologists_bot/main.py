import ast
import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from psychologists_bot.bot_events import start_bot, stop_bot
from psychologists_bot.bot.keyboards.inline import KB_SELECT_PSYCHOLOGIST
from psychologists_bot.bot.keyboards.reply import KB_START_BOT, KB_BEGIN, KB_SELECT_PSYCHO
from core.bot_config import config
from db.repositories.client import ClientRepository
from db.repositories.meet import MeetRepository
from db.repositories.psychologists import PsychologistRepository
from db.repositories.schedule import ScheduleRepository
from db.repositories.tariff import TariffRepository

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        'Привет 😉.\nЯ - бот, который поможет тебе выбрать личного психолога. Если возникнут вопросы, ты всегда можешь связаться с администратором. ' + config.ADMIN_TEXT + '\nНажми <b>"Начать"</b>, чтобы приступить к выбору',
        reply_markup=KB_START_BOT)


@dp.message_handler(commands=['support', 'help'])
async def cmd_help(message: types.Message):
    await message.answer(config.ADMIN_TEXT)


@dp.message_handler(commands=['psychologists'])
async def cmd_psychologists(message: types.Message):
    await psychologists(message)


@dp.message_handler(commands=['tariffs'])
async def cmd_tariffs(message: types.Message):
    await tariffs(message)


@dp.message_handler(commands=['meets'])
async def cmd_meets(message: types.Message):
    await client_meets(message)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(regexp='Начать')
async def begin(message: types.Message):
    await message.answer(
        '''<b>Выберите психолога, нажав на кнопку под его фотографией</b>\nНе забудьте прочитать краткое описание!\nНе переживайте, в случа чего можно будет обратиться в поддержку или выбрать пункт меню и поменять своё выбор.😉\nНажмите на кнопку или введите сообщение "выбрать"''',
        reply_markup=KB_BEGIN)


@dp.message_handler(regexp='Выбрать 🔎')
async def psychologists(message: types.Message):
    psychologist_repo: PsychologistRepository = PsychologistRepository()
    psychologists = await psychologist_repo.list()
    await message.answer('Выберите психолога, который наиболее вам подходит 😉',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Психологи', reply_markup=ReplyKeyboardRemove())
    for psychologist in psychologists:
        try:
            KB_SELECT_PSYCHOLOGIST.inline_keyboard[0][0].callback_data = str({'chosen': {'id': psychologist.id, 'n': psychologist.name, 'p': psychologist.meet_price}})
            with open('/' + psychologist.photo, 'rb') as photo:
                await message.answer_photo(photo,
                                           caption='<b>' + psychologist.name + '. Возраст ' + str(
                                               psychologist.age) + '. ' + str(psychologist.meet_price) + 'р за сеанс.</b>\n' + psychologist.description,
                                           reply_markup=KB_SELECT_PSYCHOLOGIST)
        except FileNotFoundError as e:
            logging.warning(psychologist.tg_link, psychologist.name, e)


@dp.callback_query_handler(regexp='chosen')
async def save_user_request(call: types.CallbackQuery):
    await call.message.answer('Ваша заявка сохранена, скоро с вами свяжется наш администратор 😊')
    chosen_psychologist = ast.literal_eval(call.data)['chosen']
    psychologist_id, psychologist_name, psychologists_meet_price = chosen_psychologist['id'], chosen_psychologist['n'],\
                                                                   chosen_psychologist['p']
    if call.message.chat.username is None:
        await bot.send_message(call.message.chat.id,
                               f'К сожалению, в вашем аккаунте не указана ссылка на ваш профиль, для записи к выбранному психологу, свяжитесь с нашим администратором.\n{config.ADMIN_TEXT}')
    for id in config.ADMINS_IDS:
        await bot.send_message(id, f'@{call.message.chat.username} оставил заявку на запись к психологу id: {psychologist_id} name: {psychologist_name}')


async def client_meets(message: types.Message):
    client_repo: ClientRepository = ClientRepository()
    client = await client_repo.get(str(message.chat.id))
    await message.answer(f'Количество сеансов: {client.remaining_meets}') if client and client.remaining_meets else\
        await message.answer('Вы ещё не выбрали количество сеансов 😔')


@dp.callback_query_handler(regexp='set_tariff')
async def set_tariff(call: types.CallbackQuery):
    selected_tariff_data = ast.literal_eval(call.data)['set_tariff']
    selected_tariff_name = selected_tariff_data['name']
    tariffs_repo: TariffRepository = TariffRepository()
    selected_tariff = await tariffs_repo.get(selected_tariff_name)
    await call.message.answer(
        'Вы выбрали: ' + selected_tariff.name + '\nЕсли вас всё устраивает, переходите к выбору психолога', reply_markup=KB_SELECT_PSYCHO)


@dp.message_handler()
async def undefined(message: types.Message):
    await message.answer(
        'Я не знаю такой команды 🙁. \nОбратитесь к администратору или воспользуйтесь списком команд из меню')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot, on_shutdown=stop_bot)
