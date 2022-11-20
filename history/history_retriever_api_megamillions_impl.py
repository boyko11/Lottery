import requests
from xml.etree import ElementTree
import json
from main.logger import logging
from model.lottery_history import LotteryHistory
from history.history_retriever_api import HistoryRetrieverApi


class HistoryRetrieverApiMegaMillionsImpl(HistoryRetrieverApi):

    def retrieve_history(self):
        logging.info(f'Retrieving {type} history.')

        response = requests.get(self.url)
        logging.info(f'HTTP Status Code: {response.status_code}')

        string_xml = ElementTree.fromstring(response.content)
        logging.info(f'{type} History Response: {string_xml.text}')

        json_object = json.loads(string_xml.text)

        n1_history = [this_drawing['N1'] for this_drawing in json_object['DrawingData']]
        n2_history = [this_drawing['N2'] for this_drawing in json_object['DrawingData']]
        n3_history = [this_drawing['N3'] for this_drawing in json_object['DrawingData']]
        n4_history = [this_drawing['N4'] for this_drawing in json_object['DrawingData']]
        n5_history = [this_drawing['N5'] for this_drawing in json_object['DrawingData']]

        most_recent_draw_date = json_object['DrawingData'][0]['PlayDate']

        all_numbers_history = n1_history + n2_history + n3_history + n4_history + n5_history
        special_number_history = [this_drawing['MBall']
                                  for this_drawing in json_object['DrawingData']
                                  ]

        return LotteryHistory(all_numbers_history, special_number_history, most_recent_draw_date)
