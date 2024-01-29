from datetime import datetime

import requests

from config import config
from history.history_retriever_api import HistoryRetrieverApi
from model.lottery_history import LotteryHistory


class HistoryRetrieverApiPbNyPublic(HistoryRetrieverApi):

    def retrieve_history(self):
        self.logger.info(f'Retrieving history...')

        response = requests.get(config.powerball_history_url_ny_public)

        self.logger.info(f'Powerball page url: {config.powerball_history_url_ny_public}')
        self.logger.info(f'HTTP Status Code: {response.status_code}')
        self.logger.info(f'History Response: {response.content}')

        pb_draws = response.json()

        # Rules changed on 2015-10-4
        cutoff_date = datetime(2015, 10, 4)
        pb_draws = [item for item in pb_draws if datetime.fromisoformat(item['draw_date']) > cutoff_date]

        regular_numbers_drawn = self.get_regular_numbers_drawn(pb_draws)

        powerball_numbers_drawn = self.get_powerball_numbers_drawn(pb_draws)

        most_recent_powerball_draw_date = max([draw['draw_date'] for draw in pb_draws])

        return LotteryHistory(regular_numbers_drawn, powerball_numbers_drawn, most_recent_powerball_draw_date)

    @staticmethod
    def get_regular_numbers_drawn(pb_draws):

        regular_number_draws = [drawing['winning_numbers'].split()[0:5]
                                for drawing in pb_draws]
        regular_numbers_drawn = [number_drawn for drawing in regular_number_draws for number_drawn in drawing]
        return list(map(int, regular_numbers_drawn))

    @staticmethod
    def get_powerball_numbers_drawn(pb_draws):

        powerball_numbers_drawn = [drawing['winning_numbers'].split()[5]
                                   for drawing in pb_draws]
        return list(map(int, powerball_numbers_drawn))

    def get_most_recent_date(self):
        response = requests.get(config.powerball_history_url_ny_public)

        self.logger.info(f'Powerball most recent url: {config.powerball_history_url_ny_public}')
        self.logger.info(f'HTTP Status Code: {response.status_code}')

        pb_draws = response.json()

        return max([draw['draw_date'] for draw in pb_draws])