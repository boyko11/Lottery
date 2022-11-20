from main.logger import logging
from history.history_retriever_api_megamillions_impl import HistoryRetrieverApiMegaMillionsImpl
from history.history_retriever_api_powerball_impl import HistoryRetrieverApiPowerballImpl
from main.slightly_smarter_sampler import SlightlySmarterSampler
from config import config
import sys

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: python lottery.py mega $integer_number_draws")
        print("OR:    python lottery.py power $integer_number_draws")
        print("")
        print("Examples: ")
        print("python lottery.py mega 5")
        print("Will produce 5 draws for MegaMillions.")
        print("")
        print("Examples: ")
        print("python lottery.py power 2")
        print("Will produce 2 draws for PowerBall.")
        exit(-1)

    if sys.argv[1].lower() not in ['mega', 'power']:
        print("The first arg needs to be either 'mega' or 'power'.")
        exit(-1)

    which_lotto = sys.argv[1].lower()
    num_samples = int(sys.argv[2])

    logging.info(f'Drawing {num_samples} samples for {which_lotto}...')

    history_retriever = HistoryRetrieverApiMegaMillionsImpl(config.megamillions_history_url) if which_lotto == 'mega' \
        else HistoryRetrieverApiPowerballImpl(config.powerball_history_url_template)

    history = history_retriever.retrieve_history()
    slightly_smarter_sampler = SlightlySmarterSampler(history.regular_numbers_drawn_list,
                                                      history.special_numbers_drawn_list)

    slightly_smarter_samples = slightly_smarter_sampler.sample(num_samples=num_samples)
    for sample in slightly_smarter_samples:
        print(', '.join([str(num) for num in sample['regular_numbers']]))
        print(sample['special_number'])
        print('--------')
