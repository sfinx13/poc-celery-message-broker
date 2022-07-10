from enum import Enum
import re
import json
from service.logger_decorator import LoggerDecorator as logger
from zeep import Client
from zeep.cache import InMemoryCache
from zeep.transports import Transport
from service.abstract_service import AbstractService


class NumberResponse:
    def __init__(self, status, data):
        self.status = status
        self.data = data

    def __str__(self):
        return self.data

    def to_json(self):
        return json.dumps(self, default=lambda object: object.__dict__)


class PatternResponse(Enum):
    SERVICE_TO_WORDS = r":NumberToWordsResult>(.*?)<"
    SERVICE_TO_DOLLARS = r":NumberToDollarsResult>(.*?)<"


class ConvertNumberService(AbstractService):    
    def __init__(self):
        wsdl = self.get_parameter('wsdl_number_conversion_service')
        cache = InMemoryCache(timeout=120)
        transport = Transport(cache=cache)
        self._client = Client(wsdl=wsdl, transport=transport)

    @logger('soap-logger')
    def to_words(self, number):
        """
        Returns the word corresponding to the positive number passed
        as parameter. Limited to quadrillions.
        """
        try:        
            with self._client.settings(raw_response=True):
                response = self._client.service.NumberToWords(number)
                status_code = response.status_code
                regex = PatternResponse.SERVICE_TO_WORDS.value

                data = re.findall(regex, response.text)[0]
        except Exception as err:
            status_code = 500
            data = json.dumps({})
            print(err)
        
        return NumberResponse(status_code, data)

    @logger('soap-logger')
    def to_dollars(self, number):
        """
        Returns the non-zero dollar amount of the passed number.
        """
        try:
            with self._client.settings(raw_response=True):
                response = self._client.service.NumberToDollars(number)
                status_code = response.status_code
                regex = PatternResponse.SERVICE_TO_DOLLARS.value
                data = re.findall(regex, response.text)[0]
        except Exception as err:
            status_code = 500
            data = json.dumps({})
            print(err)

        return NumberResponse(status_code, data)
