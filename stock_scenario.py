from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from c_utils import c_keyboard, get_price_in_user_currency
from db import db, get_or_create_user
import settings
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


s_list = settings.available_stock


def stock_scenario_start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f'Выбери компанию',
        reply_markup=c_keyboard(*s_list, ['Выбрать компанию по умолчанию', 'На главную'])
    )
    return "user_stock"


def get_stock_price(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_stock = update.message.text
    url = f'https://cloud.iexapis.com/stable/stock/{user_stock}/quote'
    params = {
        'token': settings.API_KEY_IEX
    }
    r = requests.get(url=url, params=params)
    r_json = r.json()
    stock_price = r_json['latestPrice']
    preset_currency = 'USD'
    stock_price_in_rub = get_price_in_user_currency(preset_currency, stock_price)
    update.message.reply_text(f'Текущая цена акций {user_stock}: {stock_price} USD ({stock_price_in_rub} руб)',
    reply_markup=c_keyboard(['Подписаться на курс этой валюты'], ['Назад'], ['На главную']))

    return 'stock_price'


def stock_subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    pass


def stock_cancel(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Возвращаемся в главное меню',
                            reply_markup=c_keyboard(*settings.main))
    return ConversationHandler.END
