import time
import xmltodict
from zeep import Client
from zeep.cache import SqliteCache, InMemoryCache
from zeep.transports import Transport
from service.abstract_service import AbstractService


class NumberResponse:
    def __init__(self, status, result):
        self.status = status
        self.result = result

    def __str__(self):
        return self.result


class ConvertNumberService(AbstractService):
    def __init__(self):
        wsdl = self.get_parameter('wsdl_number_conversion_service')
        cache = SqliteCache('sqlite.db', timeout=60)
        transport = Transport(cache=cache)
        self._client = Client(wsdl=wsdl, transport=transport)
        self._logger = self.get_logger()

    def to_words(self, number):
        """
        Returns the word corresponding to the positive number passed
        as parameter. Limited to quadrillions.
        """

        self._logger.debug(
            '[start] Request NumberToWords method({})'
            .format(number)
        )
        start = time.time()

        with self._client.settings(raw_response=True):
            response = self._client.service.NumberToWords(number)
            content = xmltodict.parse(response.text)

            status_code = response.status_code
            result = content['soap:Envelope']['soap:Body']['m:NumberToWordsResponse']['m:NumberToWordsResult']
        
        self._logger.debug(
            '[end] Response NumberToWords with status code: {}, duration: {}s'
            .format(status_code, "%.3f" % (time.time() - start))
        )

        return NumberResponse(status_code, result)

    def to_dollars(self, number):
        """
        Returns the non-zero dollar amount of the passed number.
        """
        start = time.time()
        self._logger.debug(
            '[start] Request NumberToDollars method({})'
            .format(number)
        )

        with self._client.settings(raw_response=True):
            response = self._client.service.NumberToDollars(number)
            content = xmltodict.parse(response.text)

            status_code = response.status_code
            result = content['soap:Envelope']['soap:Body']['m:NumberToDollarsResponse']['m:NumberToDollarsResult']

        self._logger.debug(
            '[end] Response NumberToDollars with status code {}, duration: {}s'
            .format(status_code, "%.3f" % (time.time() - start))
        )

        return NumberResponse(status_code, result)

