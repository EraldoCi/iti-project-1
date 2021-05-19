import sys
import pathlib
from typing import List, Dict
from compressor import Compressor
from decompressor import Decompressor
import timeit
import os
import struct
import base64


class LZW:
    def __init__(self, dictionary_size: int):
        self.dictionary_size = dictionary_size
        self.dictionary: dict
        self.reversed_dictionary: dict
        self.compressed_message: list = []

    def init_code_dictionary(self, k) -> Dict:
        dictionary_size = pow(2, k - 1)
        dictionary = {}
        for i in range(dictionary_size):
            if i < 256:
                dictionary[i.to_bytes(1, 'big')] = i
            else:
                dictionary[i.to_bytes(16, 'big')] = i
        return dictionary

    def init_decode_dictionary(self, k) -> Dict:
        dictionary_size = pow(2, k - 1)
        dictionary = {}
        for i in range(dictionary_size):
            if i < 256:
                dictionary[f'{i}'] = i.to_bytes(1, 'big')
            else:
                dictionary[f'{i}'] = i.to_bytes(16, 'big')
        return dictionary

    def compress(self, data, file_name, k):
        compressed_file = open(
            f'./data/large_inputs/compression/{file_name}.bin', 'wb')

        compressor = Compressor(
            data=data, dictionary=self.init_code_dictionary(k))
        self.compressed_message = compressor.run()

        compressed_file.write(struct.pack(
            f">{'I'*len(self.compressed_message)}", *self.compressed_message))
        compressed_file.close()
        print(
            f"\nSIZE AFTER COMPRESSION: {os.path.getsize(f'./data/large_inputs/compression/{file_name}.bin')}")

        return {
            "Message": "Finished Compression 🗜",
            "Compression file size": os.path.getsize(f'./data/large_inputs/compression/{file_name}.bin')
        }

    def decompress(self, data, k):
        decompressor = Decompressor(
            data=data, dictionary=self.init_decode_dictionary(k))
        decoded_message = decompressor.run()

        return decoded_message

    def calculate_ratio_compression(self):
        return 'compression ratio value'


'''
  Run lzw using the following comand for compressing:
  $ python lwz.py file_name.extension -c k_size
  or for decompressing
  use: $ python lwz.py file_name.extension -d k_size
'''
if __name__ == '__main__':
    root_path: str = pathlib.Path().absolute()
    _, file_name, command, dictionary_size = sys.argv
    print(_, file_name, command, dictionary_size)

    file_path: str = f'{root_path}/data/large_inputs/'

    lzw = LZW(dictionary_size)

    if command == '-c':
        with open(f"{file_path}/{file_name}", 'rb') as input_file:
            input_file_size = os.path.getsize(f"{file_path}/{file_name}")
            print(
                f"SIZE BEFORE COMPRESSION: {input_file_size}")
            compressed_data = lzw.compress(
                input_file.read(), file_name, int(dictionary_size))
            compressed_ratio = compressed_data["Compression file size"] / \
                input_file_size

    elif command == '-d':
        with open(file=f"{file_path}/compression/{file_name}.bin", mode='rb') as input_file:
            file_bytes = input_file.read()
            print(len(file_bytes))
            bytes_to_string_list = struct.unpack(
                f">{'I'*(round(len(file_bytes)/4))}", file_bytes)
            decoded_message = lzw.decompress(
                bytes_to_string_list, int(dictionary_size))
            file_for_decoded_message = open(
                file=f'./data/large_inputs/decompression/{file_name}',
                encoding='ISO-8859-1',
                mode='w'
            )

            file_for_decoded_message.write(decoded_message)
            file_for_decoded_message.close()
