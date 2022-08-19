import collections
import logging
import numpy as np
from model.numbers_and_probabilities import NumbersAndProbabilities


class SlightlySmarterSampler:

    def __init__(self, regular_history, special_number_history):
        self.regular_history = regular_history
        self.special_number_history = special_number_history

    @staticmethod
    def calculate_probabilities(history):

        numbers_counts = dict(collections.Counter(history))
        # list of tuples - first element is the number,
        # second element is the count of hom many times the number has been drawn in the past
        numbers_counts_descending = sorted(numbers_counts.items(), key=lambda x: x[1], reverse=True)

        logging.info('Numbers by descending drawings counts:')
        logging.info(numbers_counts_descending)

        number_frequencies_inverted = 1 / np.array([float(num_count_tuple[1]) for num_count_tuple in
                                                    numbers_counts_descending])
        number_next_draw_probability = number_frequencies_inverted / sum(number_frequencies_inverted)
        logging.info('number_next_draw_probability:')
        logging.info(number_next_draw_probability)

        numbers_to_draw_from = np.array([float(num_count_tuple[0]) for num_count_tuple in
                                         numbers_counts_descending])

        return NumbersAndProbabilities(numbers_to_draw_from, number_next_draw_probability)

    def sample(self, num_samples=1, num_per_samples=5):

        regular_numbers_and_probabilities = self.calculate_probabilities(self.regular_history)
        special_numbers_and_probabilities = self.calculate_probabilities(self.special_number_history)

        samples = []
        for draw_index in range(num_samples):
            drawn_numbers = np.random.choice(regular_numbers_and_probabilities.numbers, num_per_samples, replace=False,
                                             p=regular_numbers_and_probabilities.probabilities)
            drawn_numbers = np.sort(drawn_numbers)
            drawn_special_number = np.random.choice(special_numbers_and_probabilities.numbers, 1,
                                                    p=special_numbers_and_probabilities.probabilities)

            samples.append(drawn_numbers.astype(np.int))
            samples.append(drawn_special_number.astype(np.int))

        return samples
