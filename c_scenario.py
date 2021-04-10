from telegram.ext import ConversationHandler
from c_utils import c_keyboard, get_c_exchange_rate
from db import db, get_or_create_user, save_currency
import settings

c_list = settings.available_currencies


def с_scenario_start(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        'Доступные валюты:',
        reply_markup=c_keyboard(*c_list, ['На главную'])
    )
    return 'user_currency'


def c_subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_currency(db, user['user_id'], context.user_data['default_currency'])


def set_exch_currency(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    default_exch_currency = update.message.text
    update.message.reply_text('Готово')
    return default_exch_currency


def c_scenario_rate(update, context):
    context.user_data['default_currency'] = update.message.text
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    user_currency = update.message.text
    user_cur_rate = get_c_exchange_rate(user_currency)
    update.message.reply_text(f"{user_cur_rate} руб за 1 {user_currency}",
                                 reply_markup=c_keyboard(['Подписаться на курс этой валюты'],
                                ['Назад'], ['На главную']))
    return 'c_rate'


def c_cancel(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Возвращаемся в главное меню',
                            reply_markup=c_keyboard(*settings.main))
    return ConversationHandler.END
