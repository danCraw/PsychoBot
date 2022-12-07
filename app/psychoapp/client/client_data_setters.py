import pickle

from telegram import ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from psychoapp.all_constants import redis, REDIS_TEMP_TIMEOUT
from app.psychoapp.checks import client_exist
from psychoapp.client_getters import get_client
from psychoapp.constants.keyboard_constants import SELECT_TARIFF_KEYBOARD
from psychoapp.models import Tariff, Client, Meet, Psychologist
from psychoapp.redis_operations import add_client_to_redis


def select_psycho(update: Update, callback: CallbackContext):
    ReplyKeyboardRemove()
    psychologists = Psychologist.objects.all().order_by("id")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Узнать расписание", resize_keyboard=True)]])
    for p in psychologists:
        for k in reply_markup.inline_keyboard:
            k[0].callback_data = str({'show_schedule': {'psycho_id': p.id, 'psycho_name': p.name}})
        callback.bot.send_photo(chat_id=update.message.chat_id, photo=p.photo,
                                caption='<b>{name}. Возраст {age}. {meet_price}р за сеанс.</b>\n{description}'
                                .format(name=p.name, age=p.age, description=p.description, meet_price=p.meet_price,
                                        id=p.id),
                                reply_markup=reply_markup, parse_mode='html')
    ReplyKeyboardRemove()


def select_tariff(chat_id, context):
    ReplyKeyboardRemove()
    context.bot.send_message(chat_id, SELECT_TARIFF_KEYBOARD, parse_mode='html', reply_markup=SELECT_TARIFF_KEYBOARD)


def set_client_tariff(client_id, client_name, client_tariff):
    tariff = Tariff.objects.get(name=client_tariff)
    if client_exist(client_id):
        client = Client.objects.get(tg_id=client_id)
        client.tariff = tariff
        client.save()
        print(f'client {client_name} already created. Just updating tariff')
    else:
        add_client_to_redis(client_id, client_name, client_tariff)
        print(f'client {client_name} was saved in redis')


def set_client_meet(client_id, meet_id):
    client = get_client(client_id)
    if client:
        meet = Meet.objects.get(id=meet_id)
        meet.client = client
        redis.sadd((str(client_id) + '_meets'), pickle.dumps(meet))
        redis.expire((str(client_id) + '_meets'), REDIS_TEMP_TIMEOUT)
