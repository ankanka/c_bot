from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from jobs import send_hello, subscribe, unsubscribe
import settings
from db import db, get_or_create_user
from c_utils import c_keyboard
from c_scenario import с_scenario_start, c_scenario_rate, c_subscribe, c_cancel
from crypto_scenario import crypto_scenario_rate, crypto_subscribe, crypto_cancel, сrypto_scenario_start
from stock_scenario import stock_scenario_start, get_stock_price, stock_subscribe, stock_cancel

import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)

#  PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {
# 'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    print('Вызван /start')
    update.message.reply_text(
        'Привет, пользователь!',
        reply_markup=c_keyboard(*settings.main)  # c_keyboard(settings.main[0], settings.main[1], settings.main[2])
    )


def unknown(update, context):
    get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text('Не понял тебя')


def main():
    curbot = Updater(settings.API_KEY, use_context=True)

    jq = curbot.job_queue
    jq.run_repeating(send_hello, interval=5)

    dp = curbot.dispatcher

    currency = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы валют)$'), с_scenario_start)
        ],
        states={
            'user_currency': [
                MessageHandler(Filters.regex('^(На главную)$'), c_cancel),
                MessageHandler(Filters.text, c_scenario_rate),  # flatten
            ],
            'c_rate': [
                MessageHandler(Filters.regex('^(На главную)$'), c_cancel),
                MessageHandler(Filters.regex('^(Подписаться на курс этой валюты)$'), c_subscribe),
                MessageHandler(Filters.regex('^(Назад)$'), с_scenario_start)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, unknown)
        ]
    )
    crypto_currency = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы криптовалют)$'), сrypto_scenario_start)
        ],
        states={
            'user_crypto_currency': [
                MessageHandler(Filters.regex('^(На главную)$'), crypto_cancel),
                MessageHandler(Filters.text, crypto_scenario_rate)
            ],
            'crypto_rate': [
                MessageHandler(Filters.regex('^(На главную)$'), crypto_cancel),
                MessageHandler(Filters.regex('^(Подписаться на курс этой валюты)$'), crypto_subscribe),
                MessageHandler(Filters.regex('^(Назад)$'), сrypto_scenario_start)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video |
            Filters.document | Filters.location, unknown)
        ]
    )
    stock = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Курсы акций)$'), stock_scenario_start)
        ],
        states={
            'user_stock': [
                MessageHandler(Filters.regex('^(На главную)$'), stock_cancel),
                MessageHandler(Filters.text, get_stock_price)
            ],
            'stock_price': [
                MessageHandler(Filters.regex('^(Подписаться на акции этой компании)$'), stock_subscribe),
                MessageHandler(Filters.regex('^(Назад)$'), stock_scenario_start),
                MessageHandler(Filters.regex('^(На главную)$'), stock_cancel)
            ]
        },
        fallbacks=[]
    )
    dp.add_handler(crypto_currency)
    dp.add_handler(currency)
    dp.add_handler(stock)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))

    logging.info('Бот стартовал')
    curbot.start_polling()
    curbot.idle()


if __name__ == '__main__':
    main()
