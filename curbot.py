from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton #, ConversationHandler
import settings
import requests
import currency
import c_utils

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

#PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def keyboard(list1, list2, button = ['Справка']):
    return ReplyKeyboardMarkup([list1, list2, button])

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text(
        f'Привет, пользователь!',
        reply_markup = keyboard(settings.main[0], settings.main[1])  
    )

cc_list = settings.available_crypto_currencies

def get_crypto(update, context):
    update.message.reply_text(
        f'Выбери валюту',
        reply_markup = keyboard(cc_list[0], cc_list[1], ['Выбрать криптовалюту по умолчанию'])
    )
   

def default_crypto_currency(update, context):
    return user_crypto_currency
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = keyboard(c_list[0], c_list[1], ['Выбрать валюту по умолчанию'])
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
 
def default_currency(update, context):
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = keyboard(c_list[0], c_list[1])
    )

def get_cur_exchange_rate(update, context):
    user_currency = update.message.text
    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    c_rate_json = r.json()
    for crs in c_list:
        if user_currency in crs:
            user_cur_rate = c_rate_json['Valute'][user_currency]['Value']
            update.message.reply_text(f"{round(user_cur_rate, 2)} руб за 1 {user_currency}")

s_list = settings.available_stock
def get_stock(update, context):
    update.message.reply_text(
        f'Выбери компанию',
        reply_markup = keyboard(s_list[0], s_list[1], ['Выбрать компанию по умолчанию'])
    )  



def get_stock_price(update, context):
    user_stock = update.message.text
    url = 'https://cloud.iexapis.com/stable/tops'
    params = {
        'token': settings.API_KEY_IEX,
        'symbols': user_stock
    }
    r = requests.get(url=url, params=params)
    r_json = r.json()
    stock_price = r_json[0]['lastSalePrice']
    update.message.reply_text(f'Текущая цена {user_stock}: {stock_price}$')

def get_crypto_exchange_rate(update, context):
    pass

def main():
    curbot = Updater(settings.API_KEY, use_context=True)   
    dp = curbot.dispatcher

    # currency = ConversationHandler(
    #     entry_points=[
    #         MessageHandler(Filters.regex('^(Курс валют1)$'), anketa_start)
    #     ], 
    #     states={
    #         'name': [MessageHandler(Filters.text, anketa_name)],
    #         "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
    #         "comment": [
    #             CommandHandler('skip', anketa_skip),
    #             MessageHandler(Filters.text, anketa_comment)
    # ]
    #     }, 
    #     fallbacks=[]
    # )
    #dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы криптовалют)$'), get_crypto))
    dp.add_handler(MessageHandler(Filters.regex('^(BTC)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(LTC)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(BCH)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(XRP)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(Выбрать криптовалюту по умолчанию)$'), default_crypto_currency))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), get_currency))
    dp.add_handler(MessageHandler(Filters.regex('^(Выбрать валюту по умолчанию)$'), default_currency))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы акций)$'), get_stock))
    dp.add_handler(MessageHandler(Filters.regex('^(aapl)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.regex('^(yndx)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.regex('^(twtr)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.regex('^(goog)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.text, get_cur_exchange_rate))

    logging.info('Бот стартовал')
    curbot.start_polling()
    curbot.idle()

if __name__ == '__main__':
    main()


    