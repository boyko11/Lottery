import os

from flask import Flask, request

import common_constants
import config
import logging
import atexit
from cache_service import CacheService
from history.history_retriever_api_megamillions_impl import HistoryRetrieverApiMegaMillionsImpl
from history.history_retriever_api_powerball_impl import HistoryRetrieverApiPowerballImpl
from slightly_smarter_sampler import SlightlySmarterSampler
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
cache_service = CacheService()


@app.route('/pb', methods=['GET'])
def powerball():
    num_samples = request.args.get('num_samples', default=5, type=int)
    return draw_numbers(common_constants.POWERBALL, num_samples)


@app.route('/mm', methods=['GET'])
def megamillions():
    num_samples = request.args.get('num_samples', default=5, type=int)
    return draw_numbers(common_constants.MEGAMILLIONS, num_samples)


def draw_numbers(which_lotto, num_samples):

    history = cache_service.get_history(which_lotto)
    slightly_smarter_sampler = SlightlySmarterSampler(history.regular_numbers_drawn_list,
                                                      history.special_numbers_drawn_list)

    slightly_smarter_samples = slightly_smarter_sampler.sample(num_samples=num_samples)

    for sample in slightly_smarter_samples:
        sample['regular_numbers'] = ', '.join([str(num) for num in sample['regular_numbers']])

    return slightly_smarter_samples

if __name__ == "__main__":

    cache_service.get_and_cache_powerball_history()
    cache_service.get_and_cache_megamillions_history()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cache_service.refresh_when_new_numbers, trigger="interval", seconds=600)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    port = int(os.environ.get('PORT', 4637))
    app.run(debug=True, host='0.0.0.0', port=port)