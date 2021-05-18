import sys
import pathlib
from typing import List, Dict
import timeit
import numpy as np
import os
import struct
import base64


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

    def compress(self, data, file_name):
        compressed_file = open(f'./data/test/{file_name}.bin', 'wb')

        message_size = len(data)-1
        if message_size < 1:
            print('There is no content to compress!')
            return

        self.dictionary: dict = self.init_code_dictionary()

        key, index = 255, 0
        current_byte: bytes = data[0].to_bytes(1, 'big')
        next_byte: bytes

        start_time = timeit.default_timer()
        while not index + 1 > message_size + 1:
            try:
                next_byte = data[index + 1].to_bytes(1, 'big')
            except:
                next_byte = b''
            concatenated_words: bytes = data[index].to_bytes(
                1, 'big') + next_byte

            if concatenated_words in self.dictionary:
                next_index = 1

                while concatenated_words in self.dictionary:
                    next_index += 1
                    current_byte = concatenated_words
                    if index + next_index > message_size:
                        break

                    concatenated_words += data[index +
                                               next_index].to_bytes(1, 'big')

                self.compressed_message.append(
                    self.dictionary[current_byte])
                index += len(current_byte)

            else:
                self.compressed_message.append(
                    self.dictionary[current_byte])
                index += len(current_byte)

            if key <= self.dictionary_size:
                key += 1
                self.dictionary[concatenated_words] = key
                try:
                    current_byte = concatenated_words[-1:]
                except:
                    current_byte = next_byte

        end_time = timeit.default_timer()
        compressed_file.write(struct.pack(
            'h'*len(self.compressed_message), *self.compressed_message))
        compressed_file.close()
        print(
            f"\nSIZE AFTER COMPRESSION: {os.path.getsize(f'./data/test/{file_name}.bin')}")
        # print(self.compressed_message)

        return

    def decompress(self, data):
        decode_dictionary = self.init_decode_dictionary()
        decoded_message, current_index = [], "256"
        first_letter = decode_dictionary[str(data[0])]
        decoded_message.append(first_letter.decode('latin-1'))

        decode_dictionary[current_index] = first_letter

        for i in range(1, len(data)):
            code = str(data[i])
            decoded_symbol = decode_dictionary[code].decode(
                'latin-1')
            symbol = decoded_symbol[0] if len(
                decoded_symbol) else decoded_symbol

            decode_dictionary[current_index] = decode_dictionary[current_index] + \
                symbol.encode('latin-1')

            current_index = str(int(current_index) + 1)
            decode_dictionary[current_index] = decode_dictionary[code]

            decoded_message.append(
                decode_dictionary[code].decode('latin-1'))

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

    file_path: str = f'{root_path}/data/test/{file_name}'
    # print(file_path)
    lzw = LZW(dictionary_size)

    if command == '-c':
        with open(file_path, 'rb') as input_file:
            print(f"SIZE BEFORE COMPRESSION: {os.path.getsize(file_path)}")
            lzw.compress(input_file.read(), file_name)

    elif command == '-d':
        with open(file=file_path, mode='rb') as input_file:
            file_bytes = input_file.read()
            print(len(file_bytes))
            bytes_to_string_list = struct.unpack(
                'h'*(round(len(file_bytes)/2)), file_bytes)
            print(bytes_to_string_list)
            decoded_message = lzw.decompress(data=bytes_to_string_list)
            print(decoded_message)
            exit()
            file_for_decoded_message = open(
                f'{root_path}/data/test/decompress-{file_name}', 'wb')
            file_for_decoded_message.write(base64.b64decode(decoded_message))
            file_for_decoded_message.close()
