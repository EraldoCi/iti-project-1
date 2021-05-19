import math


def get_number_of_bytes_necessary_for_number(i):
    if i < 256:
        return 1
    return math.floor(math.log(i, 2)) - 6
