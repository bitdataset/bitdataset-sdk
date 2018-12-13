import datetime
from BitDatasetAPI.BitDatasetAPI import BitDatasetAPI
from BitDatasetPandas import BitDatasetPandas



api = BitDatasetAPI('YOUR API KEY')
connector = BitDatasetPandas(api)


print("Historical quotes")
data = connector.load_quotes(['OKEX:BTCUSDT', 'BITMEX:XBTUSD'], datetime.date(2018, 9, 1), datetime.date(2018, 9, 2), 5)
print(data)


print("Historical trades")
data = connector.load_trades('OKEX:BTCUSDT', datetime.date(2018, 9, 1), datetime.date(2018, 9, 2), 5)
print(data)


print("Historical OHLCV")
data = connector.load_ohlcv('OKEX:BTCUSDT', 'M1', datetime.date(2018, 9, 1), datetime.date(2018, 9, 2), 5)
print(data)


print("latest quotes")
data = connector.latest_quotes('OKEX:BTCUSDT', datetime.date(2018, 9, 1), 5)
print(data)

print("latest trades")
data = connector.latest_trades('OKEX:BTCUSDT', datetime.date(2018, 9, 1), 5)
print(data)

print("latest ohlcv")
data = connector.latest_ohlcv('OKEX:BTCUSDT', 'M1', datetime.date(2018, 9, 1), 5)
print(data)



