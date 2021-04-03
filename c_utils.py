from decimal import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
import requests


def c_keyboard(list1, list2, button = ['Справка']):
    return ReplyKeyboardMarkup([list1, list2, button])

def get_c_exchange_rate(input_currency):
    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    c_rate_json = r.json()
    cur_rate = c_rate_json['Valute'][input_currency]['Value']
    return cur_rate

#user_currency = 'USD'

def get_price_in_user_currency(received_currency, received_price):
    cur_rate = Decimal(get_c_exchange_rate(user_currency))
    cur_rate = cur_rate.quantize(Decimal("1.0000"))
    received_price = Decimal(received_price)
    received_price = received_price.quantize(Decimal("1.0000"))
    object_price = received_price * cur_rate
    object_price = object_price.quantize(Decimal("1.0000"))
    return object_price