import requests
import json
from main.logger import logging
from model.lottery_history import LotteryHistory
from history.history_retriever_api import HistoryRetrieverApi
from datetime import datetime, timedelta


class HistoryRetrieverApiPowerballImpl(HistoryRetrieverApi):

    def retrieve_history(self):
        logging.info(f'Retrieving history...')

        start_end_dates = self.build_date_ranges()

        all_time_drawing_data = []
        for start_end_date_tuple in start_end_dates:
            drawing_records_list = self.fetch_powerball_drawings_for_range(start_end_date_tuple, self.url)
            all_time_drawing_data.extend(drawing_records_list)

        # the api sometimes returns duplicates - this cleans them out
        clean_all_time_drawing_data = [this_drawing for index, this_drawing in enumerate(all_time_drawing_data)
                                       if this_drawing not in all_time_drawing_data[index + 1:]]

        regular_numbers_drawn = self.get_regular_numbers_drawn(clean_all_time_drawing_data)

        powerball_numbers_drawn = self.get_powerball_numbers_drawn(clean_all_time_drawing_data)

        most_recent_powerball_draw_date = max([drawing['field_draw_date'] for drawing in clean_all_time_drawing_data])

        return LotteryHistory(regular_numbers_drawn, powerball_numbers_drawn, most_recent_powerball_draw_date)

    @staticmethod
    def build_date_ranges():
        # powerball's api returns a max of 100 draws at a time
        # hence, we'd have to paginate the requests
        # get about 6 months (180 days) worth of data in a batch(page)

        pball_start_date = datetime(2015, 10, 7, 0, 0, 0)
        timedelta_page_size = timedelta(days=180)
        end_date = pball_start_date + timedelta_page_size
        start_end_dates = [(pball_start_date, end_date)]

        while end_date < datetime.now():
            page_start_date = end_date
            end_date = page_start_date + timedelta_page_size
            page_end_date = end_date - timedelta(seconds=1)
            start_end_dates.append((page_start_date, page_end_date))

        return start_end_dates

    @staticmethod
    def fetch_powerball_drawings_for_range(start_end_date_tuple, url_template):

        datetime_format = "%Y-%m-%d %H:%M:%S"
        page_start_date_string = start_end_date_tuple[0].strftime(datetime_format)
        page_end_date_string = start_end_date_tuple[1].strftime(datetime_format)
        page_url = url_template.format(start_datetime=page_start_date_string, end_datetime=page_end_date_string)
        response = requests.get(page_url)

        logging.info(f'Powerball page url: {page_url}')
        logging.info(f'HTTP Status Code: {response.status_code}')
        logging.info(f'History Response: {response.content}')

        drawing_records_list = json.loads(response.content)
        return drawing_records_list

    @staticmethod
    def get_regular_numbers_drawn(historic_draw_data):

        regular_number_draws = [drawing['field_winning_numbers'].split(',')[0:5]
                                for drawing in historic_draw_data]
        regular_numbers_drawn = [number_drawn for drawing in regular_number_draws for number_drawn in drawing]
        return list(map(int, regular_numbers_drawn))

    @staticmethod
    def get_powerball_numbers_drawn(historic_draw_data):

        powerball_numbers_drawn = [drawing['field_winning_numbers'].split(',')[5]
                                   for drawing in historic_draw_data]
        return list(map(int, powerball_numbers_drawn))
