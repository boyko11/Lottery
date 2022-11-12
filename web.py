from flask import Flask, request
import os

import config
from history.history_retriever_api_megamillions_impl import HistoryRetrieverApiMegaMillionsImpl
from history.history_retriever_api_powerball_impl import HistoryRetrieverApiPowerballImpl
from slightly_smarter_sampler import SlightlySmarterSampler

app = Flask(__name__)


@app.route('/pb', methods=['GET'])
def powerball():
    num_samples = request.args.get('num_samples', default=5, type=int)
    history_retriever = HistoryRetrieverApiPowerballImpl(config.powerball_history_url_template)
    return draw_numbers(history_retriever, num_samples)


@app.route('/mm', methods=['GET'])
def megamillions():
    num_samples = request.args.get('num_samples', default=5, type=int)
    history_retriever = HistoryRetrieverApiMegaMillionsImpl(config.megamillions_history_url)
    return draw_numbers(history_retriever, num_samples)


def draw_numbers(history_retriever, num_samples):

    history = history_retriever.retrieve_history()
    slightly_smarter_sampler = SlightlySmarterSampler(history.regular_numbers_drawn_list,
                                                      history.special_numbers_drawn_list)

    slightly_smarter_samples = slightly_smarter_sampler.sample(num_samples=num_samples)

    for sample in slightly_smarter_samples:
        sample['regular_numbers'] = ', '.join([str(num) for num in sample['regular_numbers']])

    return slightly_smarter_samples


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4637))
    app.run(debug=True, host='0.0.0.0', port=port)