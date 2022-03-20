import logging
import configparser
from abc import ABC


class AbstractService(ABC):
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
