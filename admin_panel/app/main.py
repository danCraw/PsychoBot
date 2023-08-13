import telebot as telebot
from beaker.ext.database import types

import config

from logic import *

bot = telebot.TeleBot(token=config.TOKEN)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_key = types.KeyboardButton("Начать")
    keyboard.add(start_key)
    welcome_text = '''<b>Что умеет этот бот?</b>\nтекст, текст, текст, текст, текст,\nтекст, текст, текст, текст, текст,\nтекст, текст, текст, текст, текст\n\n<b>Поиск личного психолога</b>\n\n\n<b>Жми начать</b>'''
    bot.send_message(m.chat.id, welcome_text, parse_mode='html', reply_markup=keyboard)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'id пользователя {phone}'.format(phone=message.chat.id))
    if message.text == 'Начать':
        welcome(bot, message)
    if message.text == 'Выбрать':
        selectPsychologist(bot, message)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
