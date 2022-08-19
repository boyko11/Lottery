import requests
from xml.etree import ElementTree
import json
from logger import logging
from model.lottery_history import LotteryHistory


class HistoryRetrieverApi:

    def __init__(self, type, url):
        self.type = type
        self.url = url
        self.page = None
        self.special_number_key = 'MBall' if type == 'MegaMillions' else None
        self.drawing_data_key = 'DrawingData'

    def retrieve_history(self):
        logging.info(f'Retrieving {type} history.')

        self.page = requests.get(self.url)
        logging.info(f'HTTP Status Code: {self.page.status_code}')

        string_xml = ElementTree.fromstring(self.page.content)
        logging.info(f'{type} History Response: {string_xml.text}')

        json_object = json.loads(string_xml.text)

        n1_history = [this_drawing['N1'] for this_drawing in json_object['DrawingData']]
        n2_history = [this_drawing['N2'] for this_drawing in json_object['DrawingData']]
        n3_history = [this_drawing['N3'] for this_drawing in json_object['DrawingData']]
        n4_history = [this_drawing['N4'] for this_drawing in json_object['DrawingData']]
        n5_history = [this_drawing['N5'] for this_drawing in json_object['DrawingData']]

        all_numbers_history = n1_history + n2_history + n3_history + n4_history + n5_history
        special_number_history = [this_drawing[self.special_number_key]
                                  for this_drawing in json_object[self.drawing_data_key]
                                  ]

        return LotteryHistory(all_numbers_history, special_number_history)
