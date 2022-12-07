from telegram import KeyboardButton, ReplyKeyboardMarkup

from psychoapp.constants.text_constants import START_BUTTON_TEXT

WELCOME_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("Выбрать")]
], resize_keyboard=True)

START_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton(START_BUTTON_TEXT)]
], resize_keyboard=True)

SCHEDULE_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("Пробное занятие")],
    [KeyboardButton("1 сеанс в неделю")],
    [KeyboardButton("3 сеанса в неделю")],
    [KeyboardButton("Свой вариант")],
], resize_keyboard=True)

SELECT_TARIFF_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("Пробное занятие")],
    [KeyboardButton("1 сеанс в неделю")],
    [KeyboardButton("3 сеанса в неделю")],
    [KeyboardButton("Свой вариант")],
], resize_keyboard=True)

SUPPORT_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("Наш сайт", callback_data='welcome')],
    [KeyboardButton("Выбрать другого психолога", callback_data='welcome')]
], esize_keyboard=True, )
