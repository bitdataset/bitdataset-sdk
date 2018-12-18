import urllib.request
import urllib.parse
import urllib.error
import gzip
import json

API_URL = 'http://api.bitdataset.com/v1%s'

class HTTPClient:
    def __init__(self, endpoint, headers = dict(), params = dict()):
        self.url = API_URL % endpoint
        self.params = params
        self.headers = headers

    def perform(self):
        resource = self.url

        if self.params:
            query_string = urllib.parse.urlencode(self.params)
            resource = '%s?%s' % (self.url, query_string)

        request = urllib.request.Request(resource, headers=self.headers)
        try:
            handler = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            if e.code == 400:
                raise BitDatasetError("Error code 400. Your request is invalid.")
            elif e.code == 401:
                raise BitDatasetError("Error code 401. Your API key is wrong.")
            elif e.code == 403:
                raise BitDatasetError("Error code 403. Your API key doesnt’t have enough privileges to access this resource.")
            elif e.code == 404:
                raise BitDatasetError("Error code 404. The specified request path could not be found.")
            elif e.code == 429:
                raise BitDatasetError("Error code 429. You have exceeded your API key rate limits.")
            elif e.code == 550:
                raise BitDatasetError("Error code 550. You requested specific single item that we don’t have.")
            else:
                raise e
        raw_response = handler.read()

        if 'Accept-Encoding' in self.headers:
            if self.headers['Accept-Encoding'] == 'deflat, gzip':
                raw_response = gzip.decompress(raw_response)

        encoding = handler.info().get_content_charset('utf-8')
        response = json.loads(raw_response.decode(encoding))
        return response

class ListExchangesRequest:
    def endpoint(self):
        return '/exchanges'

class SymbolsRequest:
    def __init__(self, query_parameters = dict()):
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/symbols'

class OHLCVListAllPeriodsRequest:
    def endpoint(self):
        return '/ohlcv/periods'

class OHLCVLatestDataRequest:
    def __init__(self, symbol_id, query_parameters = dict()):
        self.symbol_id = symbol_id
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/ohlcv/latest/%s' % self.symbol_id

class OHLCVHistoricalDataRequest:
    def __init__(self, symbol_id, query_parameters = dict()):
        self.symbol_id = symbol_id
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/ohlcv/history/%s' % self.symbol_id

class TradesLatestDataRequest:
    def __init__(self, symbol, query_parameters = dict()):
        self.symbol = symbol
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/trades/latest/%s' % self.symbol

class TradesHistoricalDataRequest:
    def __init__(self, symbol_id, query_parameters = dict()):
        self.symbol_id = symbol_id
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/trades/history/%s' % self.symbol_id

class QuotesCurrentDataRequest:
    def __init__(self, query_parameters = dict()):
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/quotes/current/'

class QuotesCurrentDataSymbolRequest:
    def __init__(self, symbol_id):
        self.symbol_id = symbol_id

    def endpoint(self):
        return '/quotes/current/%s' % self.symbol_id

class QuotesLatestDataRequest:
    def __init__(self, symbol_id, query_parameters = dict()):
        self.symbol_id = symbol_id
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/quotes/latest/%s' % self.symbol_id

class QuotesHistoricalData:
    def __init__(self, symbol_id, query_parameters = dict()):
        self.symbol_id = symbol_id
        self.query_parameters = query_parameters

    def endpoint(self):
        return '/quotes/history/%s' % self.symbol_id


class BitDatasetAPI:
    DEFAULT_HEADERS = {
        'Accept': 'application/json'
    }
    def __init__(self, api_key, headers = dict(), client_class=HTTPClient):
        self.api_key = api_key
        header_apikey = {'apikey': self.api_key}
        self.headers = {**self.DEFAULT_HEADERS, **headers, **header_apikey}
        self.client_class = client_class

    def list_exchanges(self):
        request = ListExchangesRequest()
        client = self.client_class(request.endpoint(), self.headers)
        return client.perform()

    def list_symbols(self, query_parameters = dict()):
        request = SymbolsRequest(query_parameters)
        client = self.client_class(request.endpoint(), self.headers, request.query_parameters)
        return client.perform()

    def ohlcv_list_all_periods(self):
        request = OHLCVListAllPeriodsRequest()
        client = self.client_class(request.endpoint(), self.headers)
        return client.perform()

    def ohlcv_latest_data(self,
                          symbol_id,
                          query_parameters = dict()):
        request =  OHLCVLatestDataRequest(symbol_id,
                                          query_parameters)
        client = self.client_class(request.endpoint(),
                                   self.headers,
                                   request.query_parameters)
        return client.perform()

    def ohlcv_historical_data(self,
                              symbol_id,
                              query_parameters):
        request = OHLCVHistoricalDataRequest(symbol_id, query_parameters)
        client = self.client_class(request.endpoint(),
                                   self.headers,
                                   request.query_parameters)
        return client.perform()


    def trades_latest_data(self,
                                  symbol,
                                  query_parameters = dict()):
        request = TradesLatestDataRequest(symbol, query_parameters)
        client = self.client_class(request.endpoint(),
                                   self.headers,
                                   request.query_parameters)
        return client.perform()

    def trades_historical_data(self,
                               symbol_id,
                               query_parameters = dict()):
        request = TradesHistoricalDataRequest(symbol_id, query_parameters)
        client = self.client_class(request.endpoint(),
                                   self.headers,
                                   request.query_parameters)
        return client.perform()

    def quotes_current_data(self, query_parameters = dict()):
        request = QuotesCurrentDataRequest(query_parameters)
        client = self.client_class(request.endpoint(), self.headers, request.query_parameters)
        return client.perform()

    def quotes_current_data_symbol(self,
                                   symbol_id):
        request = QuotesCurrentDataSymbolRequest(symbol_id)
        client = self.client_class(request.endpoint(), self.headers)
        return client.perform()

    def quotes_latest_data(self,
                                  symbol_id,
                                  query_parameters = dict()):
        request = QuotesLatestDataRequest(symbol_id, query_parameters)
        client = self.client_class(request.endpoint(),
                                   self.headers,
                                   request.query_parameters)
        return client.perform()

    def quotes_historical_data(self,
                               symbol_id,
                               query_parameters = dict()):
        request = QuotesHistoricalData(symbol_id, query_parameters)
        client = self.client_class(request.endpoint(),
                                   self.headers,
                                   request.query_parameters)
        return client.perform()


class BitDatasetError(Exception):
    pass