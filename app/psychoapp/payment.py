import pickle

from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardRemove, LabeledPrice


from psychoapp.all_constants import redis
from psychoapp.checks import client_exist
from psychoapp.client.client_data_vizualizators import show_client_meets, show_client_psycho
from psychoapp.client.client_getters import get_client
from psychoapp.classes import PaymentInfo
from psychoapp.commands import admin_contact
from psychoapp.constants.text_constants import SUCCESSFUL_RECORDING_TEXT
from psychoapp.redis_operations import save_client_from_redis_to_db, save_client_meets_from_redis_to_db

from config.settings import YOTOKEN


def pay(update: Update, context: CallbackContext, payment_info: PaymentInfo):
    ReplyKeyboardRemove()
    context.bot.send_invoice(chat_id=update.callback_query.message.chat_id,
                             title='Оплата',
                             description=f'Психолог {payment_info.psycho_name}, количество сеансов {payment_info.amount_meets}',
                             payload='payed',
                             provider_token=YOTOKEN,
                             currency='RUB',
                             start_parameter='test',
                             prices=[LabeledPrice(
                                  label='Руб',
                                  amount=payment_info.price*100)])


def payment_callback(update: Update, callback: CallbackContext):
    ReplyKeyboardRemove()
    query = update.pre_checkout_query
    print(update.pre_checkout_query.from_user.id)
    # check the payload, is this from your bot?
    if query.invoice_payload != "payed":
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        print('okk')
        query.answer(ok=True)
        callback.bot.send_message(chat_id=update.pre_checkout_query.from_user.id, text=SUCCESSFUL_RECORDING_TEXT)
        show_client_meets(update.pre_checkout_query.from_user.id, callback, update.pre_checkout_query.from_user.id)
        show_client_psycho(update, callback, update.pre_checkout_query.from_user.id)
        admin_contact(update, callback)
        if not client_exist:
            save_client_from_redis_to_db(update.pre_checkout_query.from_user.id)
        save_client_meets_from_redis_to_db(update.pre_checkout_query.from_user.id)
        redis.delete(update.pre_checkout_query.from_user.id)
        redis.delete(str(update.pre_checkout_query.from_user.id) + '_meets')


def get_payment_info(client_id) -> PaymentInfo:
    client = get_client(client_id)
    meets = redis.smembers(str(client_id)+'_meets')
    for m in meets:
        meet = pickle.loads(m)
    return PaymentInfo(psycho_name=meet.day_of_the_week.psychologist.name,
                       price=meet.day_of_the_week.psychologist.meet_price*len(meets),
                       amount_meets=client.tariff.meets)