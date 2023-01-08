from telegram import Update, CallbackQuery

from psychoapp.checks import client_have_tariff, client_already_have_this_meet
from psychoapp.client.client_data_setters import select_tariff, set_client_meet, select_psycho, set_client_tariff
from psychoapp.client.client_data_vizualizators import show_schedule, show_client_meets
from psychoapp.client.client_getters import get_amount_client_meets, get_amount_client_tariff_meets
from psychoapp.commands import welcome, admin_contact
from psychoapp.constants.text_constants import START_BUTTON_TEXT, SELECT_PSYCHO_BUTTON_TEXT, \
    SELECT_SCHEDULE_BUTTON_BUTTON_TEXT, SELECT_PSYCHO_AGAIN_BUTTON_TEXT, ADMIN_BUTTON_TEXT, MY_MEETS_BUTTON_TEXT
from psychoapp.payment import get_payment_info, pay


def text_listener(update: Update, context: CallbackQuery):
    tariff_selection = ['Пробное занятие', '1 сеанс в неделю',  '3 сеанса в неделю',  'Свой вариант']
    states = {
        START_BUTTON_TEXT: welcome,
        SELECT_PSYCHO_BUTTON_TEXT: select_psycho,
        SELECT_SCHEDULE_BUTTON_BUTTON_TEXT: show_schedule,
        SELECT_PSYCHO_AGAIN_BUTTON_TEXT: select_psycho,
        ADMIN_BUTTON_TEXT: admin_contact,
        MY_MEETS_BUTTON_TEXT: show_client_meets
    }
    if update.message.text == 'Мои встречи':
        show_client_meets(update.message.chat_id, context, update.message.from_user['id'])
    if update.message.text in tariff_selection:
        set_client_tariff(update.message.from_user['id'], update.message.from_user['username'], update.message.text)
        update.message.reply_text(f'Вы выбрали <b>{update.message.text}</b>\nВыберите из расписания удобное вам время', parse_mode="html")
    elif update.message.text in states.keys():
        states[update.message.text](update, context)


def inline_button_listener(update: Update, context: CallbackQuery):
    query_data = eval(update.callback_query.data)
    if 'show_schedule' in query_data:
        show_schedule(update, context, query_data['show_schedule'])
    elif 'select_tariff' in query_data:
        select_tariff(update, context)
    elif 'set_meet' in query_data:
        client_id = query_data['set_meet']['client_id']
        meet_id = query_data['set_meet']['meet_id']
        if client_have_tariff(client_id):
            if not client_already_have_this_meet(client_id, meet_id):
                if get_amount_client_meets(client_id) < get_amount_client_tariff_meets(client_id):
                    set_client_meet(client_id, meet_id)
                    show_client_meets(update.callback_query.message.chat_id, context, client_id)
                    if get_amount_client_meets(client_id) == get_amount_client_tariff_meets(client_id):
                        update.callback_query.message.reply_text('Оплатите услугу с помощью онлайн кассы или через администратора')
                        admin_contact(update, context)
                        payment_info = get_payment_info(client_id)
                        pay(update, context, payment_info)

                else:
                    update.callback_query.message.reply_text('Вы уже выбрали необходимое количество встреч')
            else:
                update.callback_query.message.reply_text('Вы уже выбрали это время')
        else:
            update.callback_query.message.reply_text(f'Для начала выберите тариф', parse_mode="html")