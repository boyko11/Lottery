import logging

import requests
from config import config, common_constants
import json
from history.history_retriever_api_powerball_impl import HistoryRetrieverApiPowerballImpl
from history.history_retriever_api_megamillions_impl import HistoryRetrieverApiMegaMillionsImpl
from xml.etree import ElementTree


class CacheService:

    def __init__(self):

        self.history = {
            common_constants.POWERBALL: None,
            common_constants.MEGAMILLIONS: None
        }

    def cache_history(self, which_lotto, history):

        self.history[which_lotto] = history

    def get_history(self, which_lotto):

        return self.history[which_lotto]

    def get_and_cache_powerball_history(self):

        logging.info("Retreiving POWERBALL history...")
        pb_history_retriever = HistoryRetrieverApiPowerballImpl(config.powerball_history_url_template)
        pb_history = pb_history_retriever.retrieve_history()
        logging.info("Retreived POWERBALL history.")
        self.cache_history(common_constants.POWERBALL, pb_history)
        logging.info("Cached POWERBALL history.")

    def get_and_cache_megamillions_history(self):

        logging.info("Retreiving MEGAMILLIONS history...")
        mm_history_retriever = HistoryRetrieverApiMegaMillionsImpl(config.megamillions_history_url)
        mm_history = mm_history_retriever.retrieve_history()
        logging.info("Retreived MEGAMILLIONS history.")
        self.cache_history(common_constants.MEGAMILLIONS, mm_history)
        logging.info("Cached MEGAMILLIONS history.")

    def refresh_when_new_numbers_powerball(self):

        response = requests.get(config.powerball_most_recent_url)

        logging.info(f'Powerball most recent url: {config.powerball_most_recent_url}')
        logging.info(f'HTTP Status Code: {response.status_code}')

        drawing_records_list = json.loads(response.content)

        most_recent_date = drawing_records_list[0]['field_draw_date']

        logging.info(f'Most recent cached date: {self.history[common_constants.POWERBALL].most_recent_draw_date:}, '
                     f'most recent drawing date: {most_recent_date}')

        if most_recent_date == self.history[common_constants.POWERBALL].most_recent_draw_date:
            logging.info('No Powerball Refresh needed.')
            return

        logging.info('Refreshing cache...')

        self.get_and_cache_powerball_history()

        logging.info('Cache refreshed.')

    def refresh_when_new_numbers_megamillions(self):

        response = requests.get(config.megamillions_most_recent_url)

        logging.info(f'MegaMillions most recent url: {config.megamillions_most_recent_url}')
        logging.info(f'HTTP Status Code: {response.status_code}')

        string_xml = ElementTree.fromstring(response.content)

        json_object = json.loads(string_xml.text)

        most_recent_date = json_object['Drawing']['PlayDate']

        logging.info(f'Most recent cached date: {self.history[common_constants.MEGAMILLIONS].most_recent_draw_date:}, '
                     f'most recent drawing date: {most_recent_date}')

        if most_recent_date == self.history[common_constants.MEGAMILLIONS].most_recent_draw_date:
            logging.info('No MegaMillions Refresh needed.')
            return

        logging.info('Refreshing cache...')

        self.get_and_cache_megamillions_history()

        logging.info('Cache refreshed.')

    def refresh_when_new_numbers(self):
        self.refresh_when_new_numbers_powerball()
        self.refresh_when_new_numbers_megamillions()
