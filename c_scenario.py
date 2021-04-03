from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from c_utils import c_keyboard, get_c_exchange_rate
from db import db, get_or_create_user
import settings
import requests

c_list = settings.available_currencies

def с_scenario_start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f'Доступные валюты:',
        reply_markup = c_keyboard(c_list[0], c_list[1], ['На главную'])
    )
    return 'user_currency'
 
def c_subscribe(update, context): #подписка на валюту
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    pass

def c_scenario_rate(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_currency = update.message.text
    user_cur_rate = get_c_exchange_rate(user_currency)
    update.message.reply_text(f"{user_cur_rate} руб за 1 {user_currency}",
    reply_markup = c_keyboard(['Подписаться на курс этой валюты'],['Назад'], ['На главную']))
    return 'c_rate'

def c_cancel(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Возвращаемся в главное меню', reply_markup = c_keyboard(settings.main[0], settings.main[1]))
    return ConversationHandler.END



