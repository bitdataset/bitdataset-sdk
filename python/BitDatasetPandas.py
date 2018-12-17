import pandas as pd
from datetime import datetime, timedelta
from collections import OrderedDict
from BitDatasetAPI.BitDatasetAPI import BitDatasetAPI

class BitDatasetPandas:

    MAX_LIMIT = 100000
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, api):
        self.api = api


    def load_quotes(self, instruments, start, end=None, limit=None):
        """
        Load quotes data
        :param instruments: str instrument or list instruments to load
        :param start: load from datetime
        :param end: load to datetime
        :param limit: limit of quotes to load
        :return: OrderedDict with data in pandas DataFrame
        """
        if not isinstance(instruments, list):
            instruments = [instruments]
        r = OrderedDict()
        for instrument in instruments:
            result_df = pd.concat(self.__load_instrument_data(instrument, start, end, limit, self.api.quotes_historical_data))
            r[instrument.upper()] = result_df
        return r


    def load_trades(self, instruments, start, end=None, limit=None):
        """
        Load trades data
        :param instruments: str instrument or list instruments to load
        :param start: load from datetime
        :param end: load to datetime
        :param limit: limit of trades to load
        :return: OrderedDict with data in pandas DataFrame
        """
        if not isinstance(instruments, list):
            instruments = [instruments]
        r = OrderedDict()
        for instrument in instruments:
            result_df = pd.concat(self.__load_instrument_data(instrument, start, end, limit, self.api.trades_historical_data))
            r[instrument.upper()] = result_df
        return r


    def load_ohlcv(self, instruments, period, start, end=None, limit=None):
        """
        Load OHLCV data
        :param instruments: str instrument or list instruments to load
        :param period: period of OHLCV bars
        :param start: load from datetime
        :param end: load to datetime
        :param limit: limit of OHLCV to load
        :return: OrderedDict with data in pandas DataFrame
        """
        if not isinstance(instruments, list):
            instruments = [instruments]
        r = OrderedDict()
        for instrument in instruments:
            result_df = pd.concat(self.__load_instrument_data(instrument, start, end, limit, self.api.ohlcv_historical_data, period))
            r[instrument.upper()] = result_df
        return r


    def latest_quotes(self, instruments, start_from, limit=None):
        """
        Load latest quotes data
        :param instruments: str instrument or list instruments to load
        :param start_from: load from datetime
        :param limit: limit of quotes to load
        :return: OrderedDict with data in pandas DataFrame
        """
        if not isinstance(instruments, list):
            instruments = [instruments]
        r = OrderedDict()
        for instrument in instruments:
            result_df = pd.concat(self.__latest_instrument_data(instrument, start_from, limit, self.api.quotes_latest_data))
            r[instrument.upper()] = result_df
        return r


    def latest_trades(self, instruments, start_from, limit=None):
        """
        Load latest trades data
        :param instruments: str instrument or list instruments to load
        :param start_from: load from datetime
        :param limit: limit of trades to load
        :return: OrderedDict with data in pandas DataFrame
        """
        if not isinstance(instruments, list):
            instruments = [instruments]
        r = OrderedDict()
        for instrument in instruments:
            result_df = pd.concat(self.__latest_instrument_data(instrument, start_from, limit, self.api.trades_latest_data))
            r[instrument.upper()] = result_df
        return r


    def latest_ohlcv(self, instruments, period, start_from, limit=None):
        """
        Load latest OHLCV data
        :param instruments: str instrument or list instruments to load
        :param period: period of OHLCV bars
        :param start_from: load from datetime
        :param limit: limit of OHLCV to load
        :return: OrderedDict with data in pandas DataFrame
        """
        if not isinstance(instruments, list):
            instruments = [instruments]
        r = OrderedDict()
        for instrument in instruments:
            result_df = pd.concat(self.__latest_instrument_data(instrument, start_from, limit, self.api.ohlcv_latest_data, period))
            r[instrument.upper()] = result_df
        return r


    def __load_instrument_data(self, instrument, start, end, limit, api_method, period=None):
        instrument_dfs = []
        while_start_date = start
        while True:
            params = {'start': while_start_date.strftime(self.DATETIME_FORMAT)[:-3]}
            if end:
                params['end'] = end.strftime(self.DATETIME_FORMAT)[:-3]

            if limit:
                limit_query = min(limit, self.MAX_LIMIT)
            else:
                limit_query = self.MAX_LIMIT
            params['limit'] = limit_query

            if period:
                params['period'] = period
            response_df = pd.DataFrame.from_dict(api_method(instrument, params))
            if not response_df.empty:
                response_df.time = pd.to_datetime(response_df.time)
                if 'localTime' in response_df:
                    response_df.localTime = pd.to_datetime(response_df.localTime)
                response_df.set_index('time', inplace=True)
                instrument_dfs.append(response_df)

            if response_df.shape[0] < self.MAX_LIMIT or response_df.empty or (limit and response_df.shape[0] >= limit):
                break
            else:
                while_start_date = response_df.index[-1] + timedelta(milliseconds=1)
                if limit:
                    limit -= response_df.shape[0]
        return instrument_dfs


    def __latest_instrument_data(self, instrument, start_from, limit, api_method, period=None):
        instrument_dfs = []
        while_start_date = start_from
        while True:
            params = {'from': while_start_date.strftime(self.DATETIME_FORMAT)[:-3]}

            if limit:
                limit_query = min(limit, self.MAX_LIMIT)
            else:
                limit_query = self.MAX_LIMIT
            params['limit'] = limit_query

            if period:
                params['period'] = period
            response_df = pd.DataFrame.from_dict(api_method(instrument, params))
            if not response_df.empty:
                response_df.time = pd.to_datetime(response_df.time)
                if 'localTime' in response_df:
                    response_df.localTime = pd.to_datetime(response_df.localTime)
                response_df.set_index('time', inplace=True)
                instrument_dfs.append(response_df)

            if response_df.shape[0] < limit_query or response_df.empty or response_df.shape[0] == limit:
                break
            else:
                while_start_date = response_df.index[-1] - timedelta(milliseconds=1)
                if limit:
                    limit -= response_df.shape[0]
        return instrument_dfs


