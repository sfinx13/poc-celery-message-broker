import configparser
from abc import ABC


class AbstractService(ABC):
    def get_parameter(self, key):
        parser = configparser.ConfigParser()
        parser.read("./config/settings.ini")

        return parser["wsdl_client"].get(key)
