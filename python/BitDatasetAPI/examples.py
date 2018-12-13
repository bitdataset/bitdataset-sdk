from BitDatasetAPI import BitDatasetAPI
import datetime

test_key = 'YOUR_API_KEY'

api = BitDatasetAPI(test_key)


exchanges = api.list_exchanges()
print('Exchanges')
for exchange in exchanges:
    print(exchange)


symbols = api.list_symbols({'filter':'BTCUSDT'})
print('BTCUSDT symbols')
for symbol in symbols:
    print(symbol)


periods = api.ohlcv_list_all_periods()
print('OHLCV periods')
for period in periods:
    print(period)


ohlcv_latest = api.ohlcv_latest_data('okex:BTCUSDT', {'period': 'M1', 'limit':5})
print('OHLCV latest')
for ohlcv in ohlcv_latest:
    print(ohlcv)


start_date = datetime.date(2018, 9, 1).isoformat()
print('historical OHLCV')
ohlcv_historical = api.ohlcv_historical_data('okex:BTCUSDT', {'period': 'M1', 'start': start_date, 'limit':5})
for ohlcv in ohlcv_historical:
    print(ohlcv)


latest_trades = api.trades_latest_data('okex:BTCUSDT', {'limit':5})
print('Latest trades')
for trade in latest_trades:
    print(trade)


historical_trades = api.trades_historical_data('okex:BTCUSDT', {'start': start_date, 'limit':5})
print('Historical trades')
for trade in historical_trades:
    print(trade)


current_quote = api.quotes_current_data({'symbols':'okex:BTCUSDT, okex:ETHUSDT'})
print("Current Quote symbols")
print(current_quote)


current_quote = api.quotes_current_data_symbol('okex:BTCUSDT')
print("Current Quote symbol")
print(current_quote)


quotes_latest_data= api.quotes_latest_data('okex:BTCUSDT', {'limit':5})
print('Latest quotes')
for quote in quotes_latest_data:
    print(quote)


quotes_historical_data = api.quotes_historical_data('okex:BTCUSDT', {'start': start_date, 'limit':5})
print('Historical quotes')
for quote in quotes_historical_data:
    print(quote)