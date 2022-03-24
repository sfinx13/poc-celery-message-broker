import time
import xmltodict
from service.logger_decorator import LoggerDecorator as logger
from zeep import Client
from zeep.cache import SqliteCache, InMemoryCache
from zeep.transports import Transport
from service.abstract_service import AbstractService


class NumberResponse:
    def __init__(self, status, data):
        self.status = status
        self.data = data

    def __str__(self):
        return self.data


class ConvertNumberService(AbstractService):
    def __init__(self):
        wsdl = self.get_parameter('wsdl_number_conversion_service')
        cache = SqliteCache('sqlite.db', timeout=60)
        transport = Transport(cache=cache)
        self._client = Client(wsdl=wsdl, transport=transport)

    @logger('soap-logger')
    def to_words(self, number):
        """
        Returns the word corresponding to the positive number passed
        as parameter. Limited to quadrillions.
        """

        with self._client.settings(raw_response=True):
            response = self._client.service.NumberToWords(number)
            content = xmltodict.parse(response.text)

            status_code = response.status_code
            data = content['soap:Envelope']['soap:Body']['m:NumberToWordsResponse']['m:NumberToWordsResult']

        return NumberResponse(status_code, data)

    @logger('soap-logger')
    def to_dollars(self, number):
        """
        Returns the non-zero dollar amount of the passed number.
        """
        with self._client.settings(raw_response=True):
            response = self._client.service.NumberToDollars(number)
            content = xmltodict.parse(response.text)

            status_code = response.status_code
            data = content['soap:Envelope']['soap:Body']['m:NumberToDollarsResponse']['m:NumberToDollarsResult']

        return NumberResponse(status_code, data)
