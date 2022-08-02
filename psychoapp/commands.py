from psychoapp.bot_button_listeners import *
from psychoapp.constants.text_constants import ADMIN_TEXT, START_TEXT, SUPPORT_TEXT
from psychoapp.constants.keyboard_constants import START_KEYBOARD, WELCOME_KEYBOARD, SUPPORT_KEYBOARD


def start(update, context):
    ReplyKeyboardRemove()
    try:
        clear(update.message.from_user.id)
    except Exception as e:
        print(e)
    admin_contact(update, context)
    context.bot.send_message(update.message.chat_id, START_TEXT, parse_mode='html', reply_markup=START_KEYBOARD)


def welcome(update, context):
    ReplyKeyboardRemove()
    update.message.reply_text(WELCOME_TEXT, parse_mode='html', reply_markup=WELCOME_KEYBOARD)
    update.message.reply_text(EXPLAIN_TEXT, parse_mode='html')


def clear(client_id):
    print('clearing')
    redis.delete(client_id)
    redis.delete(str(client_id) + '_meets')
    print('cleared')


def support(update, _):
    ReplyKeyboardRemove()
    update.message.reply_text(SUPPORT_TEXT, parse_mode='html', reply_markup=SUPPORT_KEYBOARD)


def admin_contact(update, context):
    ReplyKeyboardRemove()
    print(update)
    try:
        update.callback_query.message.reply_text(ADMIN_TEXT, parse_mode='html')
    except:
        context.bot.send_message(update.pre_checkout_query.from_user.id, ADMIN_TEXT, parse_mode='html')


def help_command(update, _):
    ReplyKeyboardRemove()
    update.message.reply_text("Используйте /start для тестирования.")