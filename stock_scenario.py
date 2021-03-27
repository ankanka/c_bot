from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from c_utils import c_keyboard
import settings
import requests


s_list = settings.available_stock

def stock_scenario_start(update, context):
    print('ok')
    update.message.reply_text(
        f'Выбери компанию',
        reply_markup = c_keyboard(s_list[0], s_list[1], ['Выбрать компанию по умолчанию', 'На главную'])
    )  
    return "user_stock"

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
 #   return 'stock_price'

def stock_scenario_default(update, context):
    update.message.reply_text('спасибо')
    pass

def s_cancel(update, context):
	update.message.reply_text('Operation canceled', reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END