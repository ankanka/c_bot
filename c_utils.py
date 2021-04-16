import decimal
from telegram import ReplyKeyboardMarkup
from requests import Session, get
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import settings


def c_keyboard(list1, list2, button=['Справка']):
    return ReplyKeyboardMarkup([list1, list2, button])


def get_c_exchange_rate(input_currency):
    r = get('https://www.cbr-xml-daily.ru/daily_json.js')
    c_rate_json = r.json()
    cur_rate = c_rate_json['Valute'][input_currency]['Value']
    return cur_rate


def get_price_in_user_currency(received_currency, received_price):
    cur_rate = decimal.Decimal(get_c_exchange_rate(received_currency))
    cur_rate = cur_rate.quantize(decimal.Decimal("1.0000"))
    received_price = decimal.Decimal(received_price)
    received_price = received_price.quantize(decimal.Decimal("1.0000"))
    object_price = received_price * cur_rate
    object_price = object_price.quantize(decimal.Decimal("1.0000"))
    return object_price


def get_crypto_price(input_crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': input_crypto,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': settings.API_KEY_COIN,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        responce = response.json()
        crypto_price = responce['data'][input_crypto]['quote']['USD']['price']
        return crypto_price
    except (ConnectionError, Timeout, TooManyRedirects):
        return 'error'
