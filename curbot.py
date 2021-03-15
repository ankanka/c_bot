from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
import requests

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

#PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text(
        f'Привет, пользователь!',
        reply_markup = main_keyboard()
    )

def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Курсы валют', 'Курсы криптовалют'], ['Курсы акций', 'Справка']])   

cc_list = settings.available_crypto_currencies

def crypto_keyboard():
    return ReplyKeyboardMarkup([
        cc_list[0], cc_list[1], ['Выбрать криптовалюту по умолчанию']
    ])

def get_crypto(update, context):
    update.message.reply_text(
        f'Выбери валюту',
        reply_markup = crypto_keyboard()
    )

def default_crypto_keyboard():
    return ReplyKeyboardMarkup([
        cc_list[0], cc_list[1]
    ])    

def default_crypto_currency(update, context):
    return user_crypto_currency
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = default_crypto_keyboard()
    )

c_list = settings.available_currencies

def currency_keyboard():
    return ReplyKeyboardMarkup([
        c_list[0], c_list[1], ['Выбрать валюту по умолчанию']
    ])

def get_currency(update, context):
    update.message.reply_text(
        f'Выбери валюту',
        reply_markup = currency_keyboard()
    )

def default_currency_keyboard():
    return ReplyKeyboardMarkup([
        c_list[0], c_list[1]
    ])    

def default_currency(update, context):
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = default_currency_keyboard()
    )

def get_cur_exchange_rate(update, context):
    user_currency = update.message.text
    c_rate = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    c_rate_json = c_rate.json()
    for crs in c_list:
        if user_currency in crs:
            update.message.reply_text(f"{c_rate_json['Valute'][user_currency]['Value']} руб за 1 {user_currency}")

def get_exchange_rate(update, context):
    pass

def main():
    curbot = Updater(settings.API_KEY, use_context=True)   
    dp = curbot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы криптовалют)$'), get_crypto))
    dp.add_handler(MessageHandler(Filters.regex('^(BTC)$'), get_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(LTC)$'), get_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(BCH)$'), get_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(XRP)$'), get_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(Выбрать криптовалюту по умолчанию)$'), default_crypto_currency))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), get_currency))
    dp.add_handler(MessageHandler(Filters.text, get_cur_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(Выбрать валюту по умолчанию)$'), default_currency))

    logging.info('Бот стартовал')
    curbot.start_polling()
    curbot.idle()

if __name__ == '__main__':
    main()


    