import logging
import configparser
import time
import xmltodict
import zeep
from zeep import Client
from zeep.cache import SqliteCache, InMemoryCache
from zeep.transports import Transport


class NumberResponse:
    def __init__(self, status, result):
        self.status = status
        self.result = result

    def __str__(self):
        return self.result


class ConvertNumberService:
    def __init__(self):
        wsdl = self.get_parameter('wsdl_number_conversion_service')
        cache = SqliteCache('sqlite.db', timeout=60)
        transport = Transport(cache=cache)
        self.__client = Client(wsdl=wsdl, transport=transport)
        self.__logger = self.get_logger()

    def to_words(self, number):
        """
        Returns the word corresponding to the positive number passed
        as parameter. Limited to quadrillions.
        """

        self.__logger.debug(
            '[start] Request NumberToWords method({})'
            .format(number)
        )
        start = time.time()

        with self.__client.settings(raw_response=True):
            response = self.__client.service.NumberToWords(number)
            content = xmltodict.parse(response.text)

            status_code = response.status_code
            result = content['soap:Envelope']
            ['soap:Body']
            ['m:NumberToWordsResponse']
            ['m:NumberToWordsResult']

        self.__logger.debug(
            '[end] Response NumberToWords with status code: {}, duration: {}s'
            .format(status_code, "%.3f" % (time.time() - start))
        )

        return NumberResponse(status_code, result)

    def to_dollars(self, number):
        """
        Returns the non-zero dollar amount of the passed number.
        """
        start = time.time()
        self.__logger.debug(
            '[start] Request NumberToDollars method({})'
            .format(number)
        )

        with self.__client.settings(raw_response=True):
            response = self.__client.service.NumberToDollars(number)
            content = xmltodict.parse(response.text)

            status_code = response.status_code
            result = content['soap:Envelope']
            ['soap:Body']
            ['m:NumberToDollarsResponse']
            ['m:NumberToDollarsResult']

        self.__logger.debug(
            '[end] Response NumberToDollars with status code {}, duration: {}s'
            .format(status_code, "%.3f" % (time.time() - start))
        )

        return NumberResponse(status_code, result)

    def get_logger(self):
        logger = logging.getLogger("soap-logger")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def get_parameter(self, key):
        parser = configparser.ConfigParser()
        parser.read("settings.ini")

        return parser["wsdl_client"].get(key)
