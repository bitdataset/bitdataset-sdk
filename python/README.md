# BitDataset pandas

Load data from BitDataset API to pandas DataFrame

Requirements:
 * Python >= 3
 * pandas

Examples:

```python
import datetime
import BitDatasetAPI
from BitDatasetPandas import BitDatasetPandas

api = BitDatasetAPI('YOUR API KEY')
connector = BitDatasetPandas(api)

# Historical quotes"
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

