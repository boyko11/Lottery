import logging
import requests
from config import config, common_constants
import json

from history.history_retriever_api_pb_ny_public import HistoryRetrieverApiPbNyPublic
# from history.history_retriever_api_powerball_impl import HistoryRetrieverApiPowerballImpl
from history.history_retriever_api_megamillions_impl import HistoryRetrieverApiMegaMillionsImpl
from xml.etree import ElementTree


class CacheService:

    def __init__(self, logger):

        self.history = {
            common_constants.POWERBALL: None,
            common_constants.MEGAMILLIONS: None
        }
        self.logger = logger

        # self.pb_history_retriever = HistoryRetrieverApiPowerballImpl(config.powerball_history_url_template, self.logger)
        self.pb_history_retriever = HistoryRetrieverApiPbNyPublic(config.powerball_history_url_ny_public, self.logger)
        self.mm_history_retriever = HistoryRetrieverApiMegaMillionsImpl(config.megamillions_history_url, self.logger)

    def cache_history(self, which_lotto, history):

        self.history[which_lotto] = history

    def get_history(self, which_lotto):

        return self.history[which_lotto]

    def get_and_cache_powerball_history(self):

        self.logger.info("Retreiving POWERBALL history...")
        pb_history = self.pb_history_retriever.retrieve_history()
        self.logger.info("Retreived POWERBALL history.")
        self.cache_history(common_constants.POWERBALL, pb_history)
        self.logger.info("Cached POWERBALL history.")

    def get_and_cache_megamillions_history(self):

        self.logger.info("Retreiving MEGAMILLIONS history...")
        mm_history = self.mm_history_retriever.retrieve_history()
        self.logger.info("Retreived MEGAMILLIONS history.")
        self.cache_history(common_constants.MEGAMILLIONS, mm_history)
        self.logger.info("Cached MEGAMILLIONS history.")

    def refresh_when_new_numbers_powerball(self):

        most_recent_date = self.pb_history_retriever.get_most_recent_date()

        self.logger.info(f'Most recent cached date: {self.history[common_constants.POWERBALL].most_recent_draw_date:}, '
                     f'most recent drawing date: {most_recent_date}')

        if most_recent_date == self.history[common_constants.POWERBALL].most_recent_draw_date:
            self.logger.info('No Powerball Refresh needed.')
            return

        self.logger.info('Refreshing cache...')

        self.get_and_cache_powerball_history()

        self.logger.info('Cache refreshed.')

    def refresh_when_new_numbers_megamillions(self):

        response = requests.get(config.megamillions_most_recent_url)

        self.logger.info(f'MegaMillions most recent url: {config.megamillions_most_recent_url}')
        self.logger.info(f'HTTP Status Code: {response.status_code}')

        string_xml = ElementTree.fromstring(response.content)

        json_object = json.loads(string_xml.text)

        most_recent_date = json_object['Drawing']['PlayDate']

        self.logger.info(f'Most recent cached date: {self.history[common_constants.MEGAMILLIONS].most_recent_draw_date:}, '
                     f'most recent drawing date: {most_recent_date}')

        if most_recent_date == self.history[common_constants.MEGAMILLIONS].most_recent_draw_date:
            self.logger.info('No MegaMillions Refresh needed.')
            return

        self.logger.info('Refreshing cache...')

        self.get_and_cache_megamillions_history()

        logging.info('Cache refreshed.')

    def refresh_when_new_numbers(self):
        self.refresh_when_new_numbers_powerball()
        self.refresh_when_new_numbers_megamillions()
