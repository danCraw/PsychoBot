import ast
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from aiogramBot.bot.keyboards.inline import KB_SHOW_SCHEDULE
from aiogramBot.bot.keyboards.reply import KB_START_BOT, KB_BEGIN
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


@dp.message_handler(regexp='Начать')
async def begin(message: types.Message):
    await message.answer(
        '''<b>Выберите психолога, нажав на кнопку под его фотографией</b>\nНе забудьте прочитать краткое описание!\nНе переживайте, в случа чего можно будет обратиться в поддержку или выбрать пункт меню и поменять своё выбор.😉\nНажмите на кнопку или введите сообщение "выбрать"''',
        reply_markup=KB_BEGIN)


@dp.message_handler(regexp='Выбрать 🔎')
async def psychologists(message: types.Message):
    psychologist_repo: PsychologistRepository = PsychologistRepository()
    psychologists = await psychologist_repo.list()
    await message.answer('Выберите психолога, желаемое количество сеансов и удобное для вас время 😉',
                         reply_markup=ReplyKeyboardRemove())
    await tariffs(message)
    await message.answer('Психологи', reply_markup=ReplyKeyboardRemove())
    for psychologist in psychologists:
        KB_SHOW_SCHEDULE.inline_keyboard[0][0].callback_data = str(
            {'schedule': {'id': psychologist.id, 'name': psychologist.name}})
        with open('../app/media/' + psychologist.photo, 'rb') as photo:
            await message.answer_photo(photo,
                                       caption='<b>' + psychologist.name + '. Возраст ' + str(
                                           psychologist.age) + '. ' + str(
                                           psychologist.meet_price) + 'р за сеанс.</b>\n' + psychologist.description,
                                       reply_markup=KB_SHOW_SCHEDULE)


@dp.callback_query_handler(regexp='schedule')
async def schedule(call: types.CallbackQuery):
    schedule_data = ast.literal_eval(call.data)['schedule']
    psychologist_id, psychologist_name = schedule_data['id'], schedule_data['name']
    schedule_repo: ScheduleRepository = ScheduleRepository()
    meet_repo: MeetRepository = MeetRepository()
    days_of_week = await schedule_repo.get_psychologist_schedule(psychologist_id)
    for day in days_of_week:
        meets = await meet_repo.get_free_meets(day.id)
        kb_day_schedule = InlineKeyboardMarkup(len(meets))
        for meet in meets:
            kb_day_schedule.add(
                InlineKeyboardButton((str(meet.time_start.strftime('%H:%M')) + '-' + str(
                    meet.time_end.strftime('%H:%M'))),
                                     callback_data=str(
                                         {'set_meet': {'meet_id': meet.id}}))
            )
        await call.message.answer('Расписание для психолога <b>' + psychologist_name + '</b> \n'
                                                                                       '<b>' + day.day_of_the_week + '</b>',
                                  reply_markup=kb_day_schedule, parse_mode='html')


async def tariffs(message: types.Message):
    tariffs_repo: TariffRepository = TariffRepository()
    tariffs = await tariffs_repo.list()
    kb_tariffs = InlineKeyboardMarkup(len(tariffs))
    for tariff in tariffs:
        kb_tariffs.add(
            InlineKeyboardButton(tariff.name, callback_data=str({'set_tariff': {'name': tariff.name}})))
    await message.answer('Выберете количество сеансов', reply_markup=kb_tariffs)


@dp.callback_query_handler(regexp='set_meet')
async def set_meet(call: types.CallbackQuery):
    client_tg_id = call.message.chat.id
    client_repo: ClientRepository = ClientRepository()
    if await client_repo.get(client_tg_id):
        await call.message.answer('Вы уже оплатили выбранное время 😊.\nВ случае ошибки, пожалуйста, свяжитесь с администратором.\n' + config.ADMIN_TEXT)
        return
    if await client_repo.have_tariff(client_tg_id):
        pass
    else:
        await call.message.answer('Пожалуйста, для начала выберите желаемое количество сеансов 😌')


@dp.callback_query_handler(regexp='set_tariff')
async def set_tariff(call: types.CallbackQuery):
    client_tg_id = call.message.chat.id
    client_repo: ClientRepository = ClientRepository()
    if await client_repo.get(client_tg_id):
        await call.message.answer('Вы уже оплатили выбранное количество встреч 😊.\nВ случае ошибки, пожалуйста, свяжитесь с администратором.\n' + config.ADMIN_TEXT)
        return
    tariff_data = ast.literal_eval(call.data)['set_tariff']
    tariff_name = tariff_data['name']
    tariffs_repo: TariffRepository = TariffRepository()
    tariff = await tariffs_repo.get(tariff_name)
    await client_repo.set_temp_tariff(client_tg_id, tariff_name)
    if await client_repo.have_tariff(client_tg_id):
        await call.message.answer('Количество сеансов изменено на ' + str(tariff.meets))
    else:
        await call.message.answer('Выбраное количество сеансов ' + str(tariff.meets))
    await call.message.answer('Если вас всё устраивает, переходите к выбору удобного вам времени')


@dp.message_handler()
async def undefined(message: types.Message):
    await message.answer(
        'Я не знаю такой команды 🙁. \nОбратитесь к администратору или воспользуйтесь списком команд из меню')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_app, on_shutdown=stop_app)
