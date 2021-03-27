from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from c_utils import c_keyboard
import settings
import requests

c_list = settings.available_currencies

def с_scenario_start(update, context):
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = c_keyboard(c_list[0], c_list[1], ['На главную'])
    )
    return 'user_currency'
 
def c_signup(update, context): #подписка на валюту
    pass


def c_scenario_rate(update, context):
    user_currency = update.message.text
    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    c_rate_json = r.json()
    user_cur_rate = c_rate_json['Valute'][user_currency]['Value']
    update.message.reply_text(f"{round(user_cur_rate, 2)} руб за 1 {user_currency}",
    reply_markup = c_keyboard(['Подписаться на курс этой валюты'],['Назад'], ['На главную']))
    return 'c_rate'

def c_cancel(update, context):
	update.message.reply_text('Operation canceled', reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END



