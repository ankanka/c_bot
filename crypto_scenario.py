
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
from c_utils import c_keyboard, get_crypto_price
from db import db, get_or_create_user
import settings
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

crypto_list = settings.available_crypto_currencies


def сrypto_scenario_start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(f'Доступные валюты:',
                              reply_markup=c_keyboard(*crypto_list, ['На главную'])
                              )
    return 'user_crypto_currency'


def crypto_subscribe(update, context): 
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    pass


def crypto_scenario_rate(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_c_currency = update.message.text
    user_cur_rate = get_crypto_price(user_c_currency)
    update.message.reply_text(f"{user_cur_rate}$ за 1 {user_c_currency}",
                              reply_markup=c_keyboard(['Подписаться на курс этой валюты'], ['Назад'], ['На главную']))
    return 'crypto_rate'


def crypto_cancel(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Возвращаемся в главное меню', reply_markup=c_keyboard(*settings.main))
    return ConversationHandler.END
