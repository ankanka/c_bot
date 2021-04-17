# Curbot

Currency & stock bot - это телеграм-бот, который поможет отслеживать курсы валют, стоимость криптовалют и котировки акций. 

Публичная ссылка: https://t.me/curstock_bot

<img src= "https://i.imgur.com/8stjupa.jpg" width = "300" height = "600" > <img src= "https://i.imgur.com/S8AN8az.jpg" width = "300" height = "600" > <img src= "https://i.imgur.com/tdHB8Bq.jpg" width = "300" height = "600" >

### Установка и настройка

1. Клонируйте репозиторий, создайте виртуальное окружение
2. Установите зависимости `pip install -r requirements.txt`
3. Создайте файл settings.py и создайте в нем переменные:
  ```
  API_KEY = "Ключ вашего бота"
  PROXY_URL = "URL socks5-прокси"

  MONGO_LINK = "Ссылка на вашу базу данных"
  MONGO_DB = "Название вашей базы"

  main = [['Курсы валют', 'Курсы криптовалют'], ['Курсы акций', 'Справка']]
  available_currencies = [['USD', 'EUR', 'JPY', 'CHF', 'BYN'], ['GBP', 'UAH', 'AMD', 'AZN', 'KZT']]
  available_crypto_currencies = [['BTC', 'LTC', 'BNB', 'ADA', 'DOT'], ['BCH', 'XRP', 'THETA', 'UNI', 'ETH']]
available_stock = [['aapl', 'twtr', 'yndx', 'goog', 'amzn'], ['snap', 'fb', 'aig', 'tsla', 'msft']]
  ```

### Запуск
Чтобы запустить бота, выполните в консоли:
```
python3 curbot.py
```
