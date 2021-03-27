from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
import requests
import currency
from c_utils import c_keyboard
from c_scenario import с_scenario_start, c_scenario_rate, c_signup, c_cancel
from stock_scenario import stock_scenario_start, get_stock_price, stock_scenario_default, s_cancel

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

#PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text(
        f'Привет, пользователь!',
        reply_markup = c_keyboard(settings.main[0], settings.main[1])  
    )

cc_list = settings.available_crypto_currencies

def get_crypto(update, context):
    update.message.reply_text(
        f'Выбери валюту',
        reply_markup = c_keyboard(cc_list[0], cc_list[1], ['Выбрать криптовалюту по умолчанию'])
    )

def default_crypto_currency(update, context):
    return user_crypto_currency
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = c_keyboard(c_list[0], c_list[1], ['Выбрать валюту по умолчанию'])
    )

def get_crypto_exchange_rate(update, context):
    pass

def unknown (update, context):
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
                MessageHandler(Filters.text, c_scenario_rate)],
            'c_rate': [
                MessageHandler(Filters.regex('^(Подписаться на курс этой валюты)$'), c_signup),
                MessageHandler(Filters.regex('^(Назад)$'), с_scenario_start),
                MessageHandler(Filters.regex('^(На главную)$'), с_scenario_start)
            ]
        }, 
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, unknown)
        ]
    )
    stock = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы акций)$'), stock_scenario_start),
            MessageHandler(Filters.regex('^(На главную)$'), s_cancel)
        ], 
        states={
            'user_stock': [MessageHandler(Filters.text, get_stock_price)],
            'stock_price': [MessageHandler(Filters.text, stock_scenario_default)]
#            "default_stock": [MessageHandler(Filters.regex('^(RUB|USD|UAH|GBP$'), c_scenario_)]
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


    