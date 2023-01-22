import ast
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, LabeledPrice
from yookassa import Configuration, Payment

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





@dp.message_handler(commands=['meets'])
async def cmd_meets(message: types.Message):
    await client_meets(message)


def payment(value, description):
    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "урл редиректа"
        },
        "capture": True,
        "description": description
    })
    return json.loads(payment.json())


async def check_payment(payment_id):
    payment = json.loads((Payment.find_one(payment_id)).json())
    while payment['status'] == 'pending':
        payment = json.loads((Payment.find_one(payment_id)).json())

    if payment['status'] == 'succeeded':
        print("SUCCSESS RETURN")
        print(payment)
        return True
    else:
        print("BAD RETURN")
        print(payment)
        return False


@dp.message_handler(commands=['buy'])
async def cmd_buy(message: types.Message):
    payment_deatils = payment(100, 'Купить товар1')
    await message.answer((payment_deatils['confirmation'])['confirmation_url'])
    if await check_payment(payment_deatils['id']):
        await message.answer("платеж")
    else:
        await message.answer("платеж не прошел")


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


@dp.callback_query_handler(regexp='set_meet')
async def set_meet(call: types.CallbackQuery):
    async def _select_meets():
        if not await client_repo.have_enough_meets(client_tg_id):
            await client_repo.set_temp_meets(client_tg_id, meet_id)
            await call.message.answer('Вы назначили сеанс:' + await generate_meet_text(meet_id))
        else:
            await call.message.answer('Вы выбрали необходимое количество сеансов')
            await client_meets(call.message)

            payment_deatils = payment.payment(100, 'Купить товар1')
            await call.message.answer((payment_deatils['confirmation'])['confirmation_url'])
            if await payment.check_payment(payment_deatils['id']):
                call.message.answer("платеж")

            else:
                call.message.answer("платеж не прошел")
    client_tg_id = call.message.chat.id
    client_repo: ClientRepository = ClientRepository()
    meet_data = ast.literal_eval(call.data)['set_meet']
    meet_id = meet_data['meet_id']
    if await client_repo.get(client_tg_id):
        await call.message.answer(
            'Вы уже оплатили выбранное время 😊.\nВ случае ошибки, пожалуйста, свяжитесь с администратором.\n' + config.ADMIN_TEXT)
        return
    if await client_repo.have_temp_tariff(client_tg_id):
        await _select_meets()
    else:
        await call.message.answer('Пожалуйста, для начала выберите желаемое количество сеансов 😌')


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
            'Вы уже оплатили выбранное количество встреч 😊.\nВ случае ошибки, пожалуйста, свяжитесь с администратором.\n' + config.ADMIN_TEXT)
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
        'Вы выбрали: ' + selected_tariff.name + '\nЕсли вас всё устраивает, переходите к выбору удобного вам времени у понраввившегося психолога')


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
