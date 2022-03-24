import logging
import time


class LoggerDecorator:
    def __init__(self, logger_type):
        self.logger_type = logger_type

        self.logger = logging.getLogger(self.logger_type)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            start = time.time()

            self.logger.debug('[start] Request {}' .format(function.__name__))

            response = function(*args, **kwargs)

            self.logger.debug('[end] Response {} duration: {}s'.format(
                function.__name__, "%.3f" % (time.time() - start))
            )

            self.logger.debug('[end] Response data {}'.format(response.data))
            return response
        return wrapper
