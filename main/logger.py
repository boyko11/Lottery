import logging
from logging.handlers import TimedRotatingFileHandler


class LotteryLogger:

    def __init__(self, log_file_path):

        self.log_file_path = log_file_path

        logging.basicConfig(
            format='%(asctime)s %(levelname)-2s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_file_path,
            encoding='utf-8')

        self.logger = logging.getLogger("Rotating LotteryLogger")
        self.logger.setLevel(logging.INFO)

        handler = TimedRotatingFileHandler(log_file_path,
                                           when="D",
                                           interval=1,
                                           backupCount=5)
        self.logger.addHandler(handler)

    def info(self, text):
        self.logger.info(text)

    def debug(self, text):
        self.logger.debug(text)
