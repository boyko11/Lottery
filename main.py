from logger import logging
from history_retriever_api import HistoryRetrieverApi
from slightly_smarter_sampler import SlightlySmarterSampler

if __name__ == '__main__':

    num_mega_samples = 5
    megamillions_history_url = "https://www.megamillions.com/cmspages/utilservice.asmx/GetDrawingPagingData?pageNumber=1&pageSize=100000&startDate=10/31/2017&endDate="

    logging.info('Lottery App started.')
    mega_history_retriever = HistoryRetrieverApi('MegaMillions', megamillions_history_url)

    mega_history = mega_history_retriever.retrieve_history()
    slightly_smarter_mega_sampler = SlightlySmarterSampler(mega_history.regular_numbers_drawn_list,
                                                           mega_history.special_numbers_drawn_list)
    mega_slightly_smarter_samples = slightly_smarter_mega_sampler.sample(num_samples=num_mega_samples)

    for index, sample in enumerate(mega_slightly_smarter_samples):
        print(sample.tolist())
        if index % 2 != 0:
            print('----')

