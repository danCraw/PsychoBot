import django
import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'psychobot/psychobot.settings'
# django.setup()
# from psychoapp.views import getAllPsychologist
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "psychobot/psychobot.settings")  # project_name название проекта
# from telebot import types
# import telebot


# def welcome(bot, message):
#     telebot.types.ReplyKeyboardRemove()
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     select_key = types.KeyboardButton("Выбрать")
#     markup.add(select_key)
#     welcome_text = '''<b>Приветственное сообщение</b>\nтекст, текст, текст, текст, текст,\nтекст, текст, текст, текст, текст,\nтекст, текст, текст, текст, текст'''
#     explain_text = '''<b>Выберте псиолога по фотографии</b>\nНе забудьте прочитать краткое описание!\nНе переживайте, в случа чего можно будет обратиться в поддержку или выбрать пункт меню и поменять своё выбор.\nНажмите выбрать'''
#     bot.send_message(message.chat.id, welcome_text, parse_mode='html', reply_markup=markup)
#     bot.send_message(message.chat.id, explain_text, parse_mode='html', reply_markup=markup)
#
#
# def selectPsychologist(bot, message):
#     psychologists = getAllPsychologist()
#     for p in psychologists:
#         bot.send_photo(message.chat.id, p.photo,
#                        caption='{name}. Возраст {age}. {number}\n{description}'
#                        .format(name=p.name, age=p.age, number=p.number, description=p.description))

# def getAllPsychologist(bot, message):
#
#     psychologists = Psychologist.objects.all()
#     for p in psychologists:
#         bot.send_photo(message.chat.id, p.photo,
#                        caption='{name}. Возраст {age}. {number}\n{description}'
#                        .format(name=p.name, age=p.age, number=p.number, description=p.description))

# def addPsychologist():
#
#
# def deletePsychologist():
#
#
# def updatePsychologist():

