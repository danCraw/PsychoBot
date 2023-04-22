import ast
import logging
import os
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from aiogramBot.bot.keyboards.inline import KB_SELECT_PSYCHOLOGIST
from aiogramBot.bot.keyboards.reply import KB_START_BOT, KB_BEGIN, KB_SELECT_PSYCHO
from aiogramBot.core.app_events import start_app, stop_app
from aiogramBot.core.config import config
from aiogramBot.db.repositories.client import ClientRepository
from aiogramBot.db.repositories.meet import MeetRepository
from aiogramBot.db.repositories.psyhologists import PsychologistRepository
from aiogramBot.db.repositories.schedule import ScheduleRepository
from aiogramBot.db.repositories.tariff import TariffRepository

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


@dp.message_handler(regexp='Выбрать психолога')
async def psychologists(message: types.Message):
    psychologist_repo: PsychologistRepository = PsychologistRepository()
    psychologists = await psychologist_repo.list()
    await message.answer('Выберите психолога, который наиболее вам подходит 😉',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Психологи', reply_markup=ReplyKeyboardRemove())
    for psychologist in psychologists:
        KB_SELECT_PSYCHOLOGIST.inline_keyboard[0][0].callback_data = str({'chosen': {'id': psychologist.id, 'n': psychologist.name, 'p': psychologist.meet_price}})
        with open('../app/media/' + psychologist.photo, 'rb') as photo:
            await message.answer_photo(photo,
                                       caption='<b>' + psychologist.name + '. Возраст ' + str(
                                           psychologist.age) + '. ' + str(psychologist.meet_price) + 'р за сеанс.</b>\n' + psychologist.description,
                                       reply_markup=KB_SELECT_PSYCHOLOGIST)


@dp.callback_query_handler(regexp='chosen')
async def save_user_request(call: types.CallbackQuery):
    await call.message.answer('Ваша заявка сохранена, скоро с вами свяжется наш администратор 😊')
    chosen_psychologist = ast.literal_eval(call.data)['chosen']
    psychologist_id, psychologist_name, psychologists_meet_price = chosen_psychologist['id'], chosen_psychologist['n'],\
                                                                   chosen_psychologist['p']
    client_repo: ClientRepository = ClientRepository()
    if await client_repo.save_temp_data_to_db(call.message.chat.id, call.message.chat.mention):
        await bot.send_message(677000194, 'что-то пошло не так, пожалуйста, свяжитесь с администратором. ' + config.ADMIN_TEXT)
    # ids = [792137742, 677000194]
    ids = [677000194]
    for id in ids:
        await bot.send_message(id, f'@{call.message.chat.username} оставил заявку на запись к психологу id: {psychologist_id} name: {psychologist_name}')


@dp.message_handler(regexp='Выбрать 🔎')
async def tariffs(message: types.Message):
    tariffs_repo: TariffRepository = TariffRepository()
    tariffs = await tariffs_repo.list()
    kb_tariffs = InlineKeyboardMarkup(len(tariffs))
    for tariff in tariffs:
        kb_tariffs.add(
            InlineKeyboardButton(tariff.name, callback_data=str({'set_tariff': {'name': tariff.name}})))
    await message.answer('Выберете количество сеансов в неделю', reply_markup=kb_tariffs)


async def client_meets(message: types.Message):
    client_tg_id = message.chat.id
    client_repo: ClientRepository = ClientRepository()
    meets = await client_repo.get_temp_meets(client_tg_id)

    message_text = 'Ваши сеансы:\n'
    if not meets:
        await message.answer('Вы ещё не назначили ни одного сеанса 😔')
        return
    for meet_id in meets:
        await message.answer(message_text + (await generate_meet_text(meet_id)))


@dp.callback_query_handler(regexp='set_tariff')
async def set_tariff(call: types.CallbackQuery):
    async def _change_temp_tariff():
        temp_tariff = await tariffs_repo.get(temp_tariff_id)
        if temp_tariff.meets != selected_tariff.meets:
            await client_repo.set_temp_tariff(client_tg_id, selected_tariff_name)
            await call.message.answer('Количество сеансов изменено на ' + str(selected_tariff.meets))
            if await client_repo.have_temp_meets(client_tg_id):
                await client_repo.delete_temp_meets(client_tg_id)
                await call.message.answer('Все назначенные встречи удалены')

    async def _set_new_temp_tariff():
        await client_repo.set_temp_tariff(client_tg_id, selected_tariff_name)
        await call.message.answer('Выбраное количество сеансов ' + str(selected_tariff.meets))

    client_tg_id = call.message.chat.id
    client_repo: ClientRepository = ClientRepository()
    if await client_repo.get(client_tg_id):
        await call.message.answer(
            'Вы уже оставляли заявку 😊.\nВ случае ошибки, пожалуйста, свяжитесь с администратором.\n' + config.ADMIN_TEXT)
        return
    selected_tariff_data = ast.literal_eval(call.data)['set_tariff']
    selected_tariff_name = selected_tariff_data['name']
    tariffs_repo: TariffRepository = TariffRepository()
    selected_tariff = await tariffs_repo.get(selected_tariff_name)
    temp_tariff_id = await client_repo.get_temp_tariff_id(client_tg_id)
    if temp_tariff_id:
        await _change_temp_tariff()
    else:
        await _set_new_temp_tariff()
    await call.message.answer(
        'Вы выбрали: ' + selected_tariff.name + '\nЕсли вас всё устраивает, переходите к выбору психолога', reply_markup=KB_SELECT_PSYCHO)


@dp.message_handler()
async def undefined(message: types.Message):
    await message.answer(
        'Я не знаю такой команды 🙁. \nОбратитесь к администратору или воспользуйтесь списком команд из меню')


# utils

async def generate_meet_text(meet_id: int):
    meet_repo: MeetRepository = MeetRepository()
    schedule_repo: ScheduleRepository = ScheduleRepository()
    meet = await meet_repo.get(int(meet_id))
    day = await schedule_repo.get(meet.day_of_the_week_id)
    time = (str(meet.time_start.strftime('%H:%M')) + '-' + str(meet.time_end.strftime('%H:%M')))
    return day.day_of_the_week + ': ' + time


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_app, on_shutdown=stop_app)
