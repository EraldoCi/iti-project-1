import math

extra_bytes = {
    "txt": -6,
    "png": -5,
    "jpeg": -2,
    "jpg": -2,
    "mp4": 2
}


def get_number_of_bytes_necessary_for_number(i, file_type):
    return 1 if i < 256 else math.floor(math.log(i, 2)) - 5
