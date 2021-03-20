from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from c_utils import c_keyboard
import settings
import requests

c_list = settings.available_currencies

def с_scenario_start(update, context):
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = c_keyboard(c_list[0], c_list[1])
    )
    return "user_currency"
 
def c_scenario_default(update, context):
    pass

def c_scenario_rate(update, context):
    user_currency = update.message.text
    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    c_rate_json = r.json()
    for crs in c_list:
        if user_currency in crs:
            user_cur_rate = c_rate_json['Valute'][user_currency]['Value']
            update.message.reply_text(f"{round(user_cur_rate, 2)} руб за 1 {user_currency}")
