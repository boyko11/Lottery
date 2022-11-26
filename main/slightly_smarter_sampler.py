import collections
import numpy as np
from model.numbers_and_probabilities import NumbersAndProbabilities


class SlightlySmarterSampler:

    def __init__(self, regular_history, special_number_history, logger):
        self.regular_history = regular_history
        self.special_number_history = special_number_history
        self.logger = logger

    def calculate_probabilities(self, history):
        numbers_counts = dict(collections.Counter(history))
        # list of tuples - first element is the number,
        # second element is the count of hom many times the number has been drawn in the past
        numbers_counts_descending = sorted(numbers_counts.items(), key=lambda x: x[1], reverse=True)

        self.logger.debug('Numbers by descending drawings counts:')
        self.logger.debug(numbers_counts_descending)

        frequencies = [float(num_count_tuple[1]) for num_count_tuple in numbers_counts_descending]

        frequencies_max = np.max(frequencies)
        frequencies_min = np.min(frequencies)
        number_frequencies_flipped = (frequencies_min + frequencies_max) - frequencies

        softmax_base = np.random.uniform(low=1.02, high=1.04)
        number_next_draw_probability = np.power(softmax_base, number_frequencies_flipped) / \
                                       np.sum(np.power(softmax_base, number_frequencies_flipped))

        self.logger.debug('number_next_draw_probability:')
        self.logger.debug(number_next_draw_probability)

        numbers_to_draw_from = np.array([float(num_count_tuple[0]) for num_count_tuple in
                                         numbers_counts_descending])

        return NumbersAndProbabilities(numbers_to_draw_from, number_next_draw_probability, softmax_base)

    def sample(self, num_samples=1, num_per_samples=5):
        regular_numbers_and_probabilities = self.calculate_probabilities(self.regular_history)
        special_numbers_and_probabilities = self.calculate_probabilities(self.special_number_history)

        samples = []
        for draw_index in range(num_samples):
            drawn_numbers = np.random.choice(regular_numbers_and_probabilities.numbers, num_per_samples, replace=False,
                                             p=regular_numbers_and_probabilities.probabilities)
            drawn_numbers = np.sort(drawn_numbers)
            drawn_special_number = np.random.choice(special_numbers_and_probabilities.numbers, 1,
                                                    p=special_numbers_and_probabilities.probabilities)[0]
            sample = {
                "regular_numbers": drawn_numbers.astype(np.int).tolist(),
                "special_number": drawn_special_number.astype(np.int).item()
            }

            samples.append(sample)

        return {
            "samples": samples,
            "softmax_base": {
                "regular": regular_numbers_and_probabilities.softmax_base,
                "special": special_numbers_and_probabilities.softmax_base
            }
        }
