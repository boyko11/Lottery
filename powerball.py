import numpy as np

number_of_draws = 5

number_frequencies = {
    61: 75, 32: 74, 21: 71, 63: 71, 23: 68, 39: 68,
    69: 67, 62: 66, 59: 64, 20: 63, 36: 63, 53: 63, 3: 62,
    10: 62, 27: 62, 28: 62, 64: 62, 37: 61,
    40: 59, 17: 58, 41: 58, 52: 58, 6: 57, 14: 57,
    16: 57, 33: 57, 44: 57, 56: 57, 12: 56, 15: 56, 18: 56,
    57: 56, 47: 56, 8: 55, 22: 55, 1: 54,
    2: 54, 42: 54, 45: 54, 67: 54, 50: 53, 54: 53,
    68: 53, 5: 52, 38: 52, 48: 52, 7: 51, 11: 51,
    30: 51, 65: 51, 19: 50, 25: 50, 29: 50, 55: 50,
    58: 50, 66: 50, 31: 49, 43: 47, 51: 47, 60: 47,
    9: 46, 49: 46, 4: 45, 26: 43, 35: 43, 46: 42,
    13: 41, 34: 41, 24: 40
}
number_frequencies_inverted = 1 / np.array([float(num) for num in number_frequencies.values()])
number_next_draw_probability = number_frequencies_inverted / sum(number_frequencies_inverted)

power_number_frequencies = {
    24: 43, 18: 40, 4: 35, 21: 34, 13: 33, 10: 32,
    26: 32, 3: 31, 6: 31, 8: 31, 19: 31, 5: 29, 9: 29,
    11: 29, 17: 29, 14: 28, 2: 27, 25: 27,
    1: 26, 22: 26, 16: 25, 20: 25, 15: 24, 7: 23,
    12: 23, 23: 20
}

power_number_frequencies_inverted = 1 / np.array([float(num) for num in power_number_frequencies.values()])
power_number_next_draw_probability = power_number_frequencies_inverted / sum(power_number_frequencies_inverted)


numbers_to_draw_from = np.array([float(num) for num in number_frequencies.keys()])
power_numbers_to_draw_from = np.array([float(num) for num in power_number_frequencies.keys()])


for draw_index in range(number_of_draws):
    drawn_numbers = np.random.choice(numbers_to_draw_from, 5, replace=False,
                                    p=number_next_draw_probability)
    drawn_numbers = np.sort(drawn_numbers)
    drawn_power_number = np.random.choice(power_numbers_to_draw_from, 1, p=power_number_next_draw_probability)

    print(drawn_numbers)
    print(drawn_power_number)
    print('--------')