# BitDataset python
It contains a BitDatasetAPI for simple api queries. And BitDataset-pandas to load data into pandas DataFrame

# Installation

```
pip install bitdataset
```

# Examples BitDatasetAPI

```python
import datetime
from bitdataset import BitDatasetAPI

test_key = 'YOUR_API_KEY'
api = BitDatasetAPI(test_key)


# Exchanges
exchanges = api.list_exchanges()
for exchange in exchanges:
    print(exchange)


# BTCUSDT symbols
symbols = api.list_symbols({'filter':'BTCUSDT'})
for symbol in symbols:
    print(symbol)


# OHLCV periods
periods = api.ohlcv_list_all_periods()
for period in periods:
    print(period)


# OHLCV latest
ohlcv_latest = api.ohlcv_latest_data('okex:BTCUSDT', {'period': 'M1', 'limit':5})
for ohlcv in ohlcv_latest:
    print(ohlcv)


# historical OHLCV
start_date = datetime.date(2018, 9, 1).isoformat()
ohlcv_historical = api.ohlcv_historical_data('okex:BTCUSDT', {'period': 'M1', 'start': start_date, 'limit':5})
for ohlcv in ohlcv_historical:
    print(ohlcv)


# Latest trades
latest_trades = api.trades_latest_data('okex:BTCUSDT', {'limit':5})
for trade in latest_trades:
    print(trade)


# Historical trades
historical_trades = api.trades_historical_data('okex:BTCUSDT', {'start': start_date, 'limit':5})
for trade in historical_trades:
    print(trade)


# Current Quote symbols
current_quote = api.quotes_current_data({'symbols':'okex:BTCUSDT, okex:ETHUSDT'})
print(current_quote)


current_quote = api.quotes_current_data_symbol('okex:BTCUSDT')
print("Current Quote symbol")
print(current_quote)


# Latest quotes
quotes_latest_data= api.quotes_latest_data('okex:BTCUSDT', {'limit':5})
for quote in quotes_latest_data:
    print(quote)


# Historical quotes
quotes_historical_data = api.quotes_historical_data('okex:BTCUSDT', {'start': start_date, 'limit':5})
for quote in quotes_historical_data:
    print(quote)

```


# Examples BitDataset-pandas

```python
import datetime
from bitdataset import BitDatasetAPI, BitDatasetPandas


api = BitDatasetAPI('YOUR API KEY')
connector = BitDatasetPandas(api)


# Historical quotes
data = connector.load_quotes(['OKEX:BTCUSDT', 'BITMEX:XBTUSD'], datetime.date(2018, 9, 1), datetime.date(2018, 9, 2), 5)
print(data)


# Historical trades
data = connector.load_trades('OKEX:BTCUSDT', datetime.date(2018, 9, 1), datetime.date(2018, 9, 2), 5)
print(data)


# Historical OHLCV
data = connector.load_ohlcv('OKEX:BTCUSDT', 'M1', datetime.date(2018, 9, 1), datetime.date(2018, 9, 2), 5)
print(data)


# Latest quotes
data = connector.latest_quotes('OKEX:BTCUSDT', datetime.date(2018, 9, 1), 5)
print(data)


# Latest trades
data = connector.latest_trades('OKEX:BTCUSDT', datetime.date(2018, 9, 1), 5)
print(data)


# Latest ohlcv
data = connector.latest_ohlcv('OKEX:BTCUSDT', 'M1', datetime.date(2018, 9, 1), 5)
print(data)


```
