from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings
import requests
import currency
from c_utils import c_keyboard
from c_scenario import с_scenario_start, c_scenario_rate, c_scenario_default

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


s_list = settings.available_stock
def get_stock(update, context):
    update.message.reply_text(
        f'Выбери компанию',
        reply_markup = c_keyboard(s_list[0], s_list[1], ['Выбрать компанию по умолчанию'])
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

    currency = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы валют)$'), с_scenario_start)
        ], 
        states={
            'user_currency': [MessageHandler(Filters.text, c_scenario_rate)],
            'rate': [MessageHandler(Filters.text, c_scenario_default)]
#            "default_currency": [MessageHandler(Filters.regex('^(RUB|USD|UAH|GBP$'), c_scenario_)]
        }, 
        fallbacks=[]
    )
    dp.add_handler(currency)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы криптовалют)$'), get_crypto))
    dp.add_handler(MessageHandler(Filters.regex('^(BTC)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(LTC)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(BCH)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(XRP)$'), get_crypto_exchange_rate))
    dp.add_handler(MessageHandler(Filters.regex('^(Выбрать криптовалюту по умолчанию)$'), default_crypto_currency))
    #dp.add_handler(MessageHandler(Filters.regex('^(Курсы валют)$'), get_currency))
    #dp.add_handler(MessageHandler(Filters.regex('^(Выбрать валюту по умолчанию)$'), default_currency))
    dp.add_handler(MessageHandler(Filters.regex('^(Курсы акций)$'), get_stock))
    dp.add_handler(MessageHandler(Filters.regex('^(aapl)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.regex('^(yndx)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.regex('^(twtr)$'), get_stock_price))
    dp.add_handler(MessageHandler(Filters.regex('^(goog)$'), get_stock_price))
    #dp.add_handler(MessageHandler(Filters.text, get_cur_exchange_rate))

    logging.info('Бот стартовал')
    curbot.start_polling()
    curbot.idle()

if __name__ == '__main__':
    main()


    