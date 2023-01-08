import pickle

from telegram import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from psychoapp.all_constants import redis
from psychoapp.constants.keyboard_constants import SELECT_TARIFF_KEYBOARD
from psychoapp.models import Schedule, Meet
from psychoapp.client.client_getters import get_client_psycho_tg_link


def show_client_meets(chat_id, callback, client_id):
    meets = redis.smembers((str(client_id) + '_meets'))
    callback.bot.send_message(chat_id, 'Ваши сеансы:')
    for m in meets:
        m = pickle.loads(m)
        callback.bot.send_message(chat_id, f"{m.day_of_the_week.day_of_the_week}\n{m.time_start.strftime('%H:%M')}-{m.time_end.strftime('%H:%M')}")


def show_client_base_meets(update, callback):
    chat_id = update.message.chat_id
    meets = redis.smembers((str(chat_id) + '_meets'))
    callback.bot.send_message(chat_id, 'Ваши сеансы:')
    for m in meets:
        m = pickle.loads(m)
        callback.bot.send_message(chat_id, f"{m.day_of_the_week.day_of_the_week}\n{m.time_start.strftime('%H:%M')}-{m.time_end.strftime('%H:%M')}")


def show_client_psycho(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f'Ваш психолог {get_client_psycho_tg_link(update.message.chat_id)}', parse_mode='html')


def show_schedule(update, context, psycho_info):
    ReplyKeyboardRemove()
    show_schedule_text = f'''Расписание для психолога {psycho_info['psycho_name']}'''
    update.callback_query.message.reply_text(show_schedule_text, parse_mode='html', reply_markup=SELECT_TARIFF_KEYBOARD)
    schedule = Schedule.objects.all().filter(psychologist=psycho_info['psycho_id'])
    schedule_buttons = InlineKeyboardMarkup([])
    have_free_time = False
    if schedule:
        for day_of_week in schedule:
            meets = Meet.objects.all().filter(day_of_the_week=day_of_week, client_id=None)
            for m in meets:
                schedule_buttons.inline_keyboard.append([InlineKeyboardButton(f"{m.time_start.strftime('%H:%M')}-{m.time_end.strftime('%H:%M')}",
                                                                              callback_data=str({'set_meet': {'meet_id': m.id, 'client_id': update.callback_query.from_user.id}}),
                                                                              resize_keyboard=True)])
                if meets:
                    have_free_time = True
                    update.callback_query.message.reply_text(f'<b>{day_of_week.day_of_the_week}</b>',
                                                             reply_markup=schedule_buttons, parse_mode='html')
                schedule_buttons.inline_keyboard = []

    if not have_free_time:
        update.callback_query.message.reply_text(f'К сожалению, свободного времени нет',
                                                 reply_markup=schedule_buttons, parse_mode='html')