from django.core.management import BaseCommand
from telegram import Bot
from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, Filters
from telegram.utils.request import Request

from app.psychoapp.bot_button_listeners import *
from psychoapp.client.client_data_setters import *
from psychoapp.client_data_vizualizators import show_schedule
from psychoapp.commands import *
from psychoapp.constants.text_constants import *
from psychoapp.payment import pay, payment_callback
from app.psychobot import settings


class Command(BaseCommand):
    help = 'telegram bot'

    def handle(self, *args, **options):
        request = Request(connect_timeout=1, read_timeout=1)
        bot = Bot(request=request, token=settings.TOKEN)
        print(bot.get_me())
        updater = Updater(bot=bot, use_context=True)
        app = updater.dispatcher
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('welcome', welcome))
        app.add_handler(CommandHandler('select_psycho', select_psycho))
        app.add_handler(CommandHandler('select_tariff', select_tariff))
        app.add_handler(CommandHandler('show_schedule', show_schedule))
        app.add_handler(CommandHandler('pay', pay))
        app.add_handler(CommandHandler('support', support))
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(PreCheckoutQueryHandler(payment_callback))

        app.add_handler(CallbackQueryHandler(inline_button_listener))
        print('текст:', Filters.text)
        app.add_handler(MessageHandler(Filters.text, text_listener))

        updater.start_polling()
        updater.idle()