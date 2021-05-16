import sys
import pathlib
from typing import List, Dict
import timeit
import numpy as np


class LZW:
    def __init__(self, dictionary_size: int):
        self.dictionary_size = dictionary_size
        self.dictionary: dict
        self.reversed_dictionary: dict
        self.compressed_message: list = []

    def init_code_dictionary(self) -> Dict:
        return {(i.to_bytes(1, 'big')): i for i in range(256)}

    def init_decode_dictionary(self) -> Dict:
        return {f'{i}': (i.to_bytes(1, 'big')) for i in range(256)}

    def compress(self, data: List[str]) -> None:
        compressed_file = open('./data/test.bin', 'w')

        message_size = len(data)-1
        if message_size < 1:
            print('There is no content to compress!')
            return

        if isinstance(data, str):
            data = data.encode()

        self.dictionary: dict = self.init_code_dictionary()

        key, index = 255, 0
        first_byte: bytes = data[0].to_bytes(1, 'big')
        next_byte: bytes

        dictionary_overflow = index + 1 > message_size

        start_time = timeit.default_timer()
        while not dictionary_overflow:
            next_byte = data[index + 1].to_bytes(1, 'big')
            concatenated_words: bytes = data[index].to_bytes(
                1, 'big') + next_byte

            if concatenated_words in self.dictionary:
                next_index = 1

                while concatenated_words in self.dictionary:
                    next_index += 1
                    first_byte = concatenated_words
                    if index + next_index > message_size:
                        break

                    concatenated_words += data[index +
                                               next_index].to_bytes(1, 'big')

                self.compressed_message.append(
                    str(self.dictionary[first_byte]))
                index += len(first_byte)

            else:
                self.compressed_message.append(
                    str(self.dictionary[first_byte]))
                first_byte = next_byte
                index += len(first_byte)

            if key <= self.dictionary_size:
                key += 1
                self.dictionary[concatenated_words] = key

            dictionary_overflow = index + 1 > message_size

        end_time = timeit.default_timer()
        print(f'Execution time: {end_time - start_time}s')

        separator: str = ','
        compressed_file.write(separator.join(self.compressed_message))
        compressed_file.close()

        print(self.compressed_message)
        return

    def decompress(self, data):
        decode_dictionary = self.init_decode_dictionary()
        decoded_message, current_index = [], "256"
        first_letter = decode_dictionary[data[0]]
        decoded_message.append(first_letter.decode('UTF-8'))

        decode_dictionary[current_index] = first_letter

        for i in range(1, len(data)):
            code = data[i]
            decoded_symbol = decode_dictionary[code].decode('UTF-8')
            symbol = decoded_symbol[0] if len(
                decoded_symbol) else decoded_symbol

            decode_dictionary[current_index] = decode_dictionary[current_index] + \
                symbol.encode('UTF-8')

            current_index = str(int(current_index) + 1)
            decode_dictionary[current_index] = decode_dictionary[code]

            decoded_message.append(decode_dictionary[code].decode('UTF-8'))

        return "".join(decoded_message)

    def calculate_ratio_compression(self):
        return 'compression ratio value'


'''
  Run lzw using the following comand for compressing:
  $ python lwz.py file_name.extension -c k_size
  or for decompressing
  use: $ python lwz.py file_name.extension -d k_size
'''
if __name__ == '__main__':
    # lzw = LZW(256)
    # print(lzw.decompress(['97', '97', '98', '257', '259', '256']))

    root_path: str = pathlib.Path().absolute()
    _, file_name, command, dictionary_size = sys.argv
    try:
        dictionary_size = 2**int(dictionary_size)
    except:
        dictionary_size = 2**9

    file_path: str = f'{root_path}/data/{file_name}'
    print(file_path)
    lzw = LZW(dictionary_size)

    if command == '-c':
        with open(file_path, 'rb') as input_file:
            lzw.compress(input_file.read())
    elif command == '-d':
        with open('./data/test.bin', 'rb') as input_file:
            file_bytes = input_file.readline()
            splitted_byte = str(file_bytes).split(',')

            splitted_byte[0] = splitted_byte[0][2:]
            splitted_byte[-1] = splitted_byte[-1][:-1]

            print(lzw.decompress(data=splitted_byte))

    # with open('./data/compressed_file.txt', 'rb') as input_file:
    #     while byte := input_file.read(1)
    #         print()
