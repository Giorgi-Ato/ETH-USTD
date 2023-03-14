import ccxt
import time
import numpy as np

# создаем объект биржи Binance
exchange = ccxt.binance()

# устанавливаем пару торгов ETH/USDT и BTC/USDT и интервал свечей в 1 минуту
timeframe = '1m'
eth_symbol = 'ETH/USDT'
btc_symbol = 'BTC/USDT'

# устанавливаем период для скользящего среднего в 60 минут
period = 60

# инициализируем переменные для хранения предыдущей цены и времени
previous_price = None
previous_time = None

while True:
    # получаем последнюю свечу с биржи Binance
    candles = exchange.fetch_ohlcv(eth_symbol, timeframe)
    last_candle = candles[-1]

    # получаем текущую цену из последней свечи
    price = last_candle[4]

    # получаем текущее время в формате timestamp
    current_time = time.time()

    # получаем данные по ценам фьючерсов ETHUSDT и BTCUSDT
    eth_candles = exchange.fetch_ohlcv(eth_symbol, timeframe)
    btc_candles = exchange.fetch_ohlcv(btc_symbol, timeframe)

    # получаем массивы цен закрытия для каждого инструмента
    eth_prices = np.array([candle[4] for candle in eth_candles])
    btc_prices = np.array([candle[4] for candle in btc_candles])

    # вычисляем коэффициент корреляции между ценами фьючерсов ETHUSDT и BTCUSDT
    correlation_coefficient = np.corrcoef(eth_prices, btc_prices)[0, 1]

    # если это первый проход цикла, сохраняем текущую цену и время
    if previous_price is None:
        previous_price = price
        previous_time = current_time
    else:
        # вычисляем разницу между текущей и предыдущей ценами
        price_diff = price - previous_price

        # вычисляем процентное изменение цены
        price_percent_change = (price_diff / previous_price) * 100

        # если процентное изменение цены более 1% за последние 60 минут, выводим сообщение в консоль
        if price_percent_change >= 1 and current_time - previous_time >= period * 60 and correlation_coefficient < 0.5:
            print(f"Цена фьючерса ETHUSDT изменилась на {price_percent_change:.2f}% за последние 60 минут.")

        # сохраняем текущую цену и время
        previous_price = price
        previous_time = current_time

    # ждем 1 минуту перед получением новых данных
    time.sleep(60)
