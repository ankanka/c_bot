from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import currency
import settings
import requests
from db import db, get_or_create_user
from c_utils import c_keyboard
from c_scenario import с_scenario_start, c_scenario_rate, c_subscribe, c_cancel
from stock_scenario import stock_scenario_start, get_stock_price, stock_subscribe, stock_cancel

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

#PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print('Вызван /start')
    update.message.reply_text(
        f'Привет, пользователь!',
        reply_markup = c_keyboard(*settings.main) # c_keyboard(settings.main[0], settings.main[1], settings.main[2]) 
    )

cc_list = settings.available_crypto_currencies

def get_crypto(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f'Выбери валюту',
        reply_markup = c_keyboard(cc_list[0], cc_list[1], ['Выбрать криптовалюту по умолчанию'])
    )

def default_crypto_currency(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    return user_crypto_currency
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = c_keyboard(c_list[0], c_list[1], ['Выбрать валюту по умолчанию'])
    )

def get_crypto_exchange_rate(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    pass

def unknown (update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Не понял тебя')

def main():
    curbot = Updater(settings.API_KEY, use_context=True)   
    dp = curbot.dispatcher

    currency = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы валют)$'), с_scenario_start),
            MessageHandler(Filters.regex('^(На главную)$'), c_cancel),
        ], 
        states={
            'user_currency': [
                MessageHandler(Filters.regex('^(На главную)$'), c_cancel),
                MessageHandler(Filters.text, c_scenario_rate), #flatten
            ],
            'c_rate': [
                MessageHandler(Filters.regex('^(Подписаться на курс этой валюты)$'), c_subscribe),
                MessageHandler(Filters.regex('^(Назад)$'), с_scenario_start),
                MessageHandler(Filters.regex('^(На главную)$'), c_cancel)
            ]
        }, 
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, unknown)
        ]
    )
    stock = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы акций)$'), stock_scenario_start),
            MessageHandler(Filters.regex('^(На главную)$'), stock_cancel)
        ], 
        states={
            'user_stock': [MessageHandler(Filters.text, get_stock_price)],
            'stock_price': [
                MessageHandler(Filters.regex('^(Подписаться на акции этой компании)$'), stock_subscribe),
                MessageHandler(Filters.regex('^(Назад)$'), stock_scenario_start),
                MessageHandler(Filters.regex('^(На главную)$'), stock_scenario_start)
            ]
        }, 
        fallbacks=[]
    )
    dp.add_handler(currency)
    dp.add_handler(stock)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы криптовалют)$'), get_crypto))
    dp.add_handler(MessageHandler(Filters.regex('^(BTC)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(LTC)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(BCH)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(XRP)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(Выбрать криптовалюту по умолчанию)$'), default_crypto_currency))

    logging.info('Бот стартовал')
    curbot.start_polling()
    curbot.idle()

if __name__ == '__main__':
    main()


    